# 02 - Transcrição

## Objetivo

Converter o áudio da live em texto com timestamps para que o restante do sistema consiga analisar falas, gerar legendas, detectar highlights e planejar cortes.

## Onde Acontece

Arquivos principais:

```text
main.py
src/transcription/whisper_transcriber.py
src/transcription/text_cleaner.py
src/transcription/transcript_schema.py
src/config/settings.py
```

## Entrada

```text
cache/audio/<nome_do_video>.wav
```

## Saída

```text
cache/transcripts/<nome_do_audio>_transcript.json
```

Formato final:

```json
{
  "source_audio": "cache/audio/live.wav",
  "language": "pt",
  "duration": 3441.21,
  "segments": [
    {
      "start": 12.4,
      "end": 16.8,
      "text": "mano, não acredito nisso!"
    }
  ]
}
```

## Como Atua Hoje

1. Valida se o arquivo de áudio existe, é `.wav` e não está vazio.
2. Define a saída em `cache/transcripts/`.
3. Se o transcript já existe e `force=False`, reaproveita o cache.
4. Carrega o `faster-whisper`.
5. Usa as configurações do `.env`.
6. Chama `model.transcribe()`.
7. Percorre os segmentos retornados pelo Whisper.
8. Limpa cada texto com `clean_transcript_text()`.
9. Remove segmentos sem texto.
10. Salva o JSON final.

## Configuração Atual

```text
WHISPER_MODEL=tiny
WHISPER_LANGUAGE=pt
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
WHISPER_CPU_THREADS=0
WHISPER_NUM_WORKERS=2
WHISPER_BEAM_SIZE=1
WHISPER_BEST_OF=1
WHISPER_VAD_FILTER=true
WHISPER_CONDITION_ON_PREVIOUS_TEXT=false
```

No código atual, a transcrição também roda com:

```python
word_timestamps=True
```

O transcript salvo hoje não guarda timestamps por palavra, apenas timestamps por segmento.

## Cache

Usa cache. Se o transcript existe, a transcrição inteira é pulada.

## Tempo Observado

Na execução limpa com vídeo de `57min21s`:

```text
Tempo aproximado: ~6min50s
Segmentos gerados: 1302
```

Foi o maior gargalo do pipeline.

## Gargalos

Prioridade altíssima.

Motivos:

- A transcrição escala com a duração do vídeo.
- Para lives de `5-6h`, pode passar de `40min` se escalar de forma linear.
- `word_timestamps=True` provavelmente adiciona custo sem uso direto no JSON final.
- O processo atual gera um transcript único; se falhar no meio, não há cache parcial por bloco.

## Pontos De Otimização

Prioridade sugerida:

1. Medir tempo real da transcrição no log.
2. Tornar `word_timestamps` configurável e testar com `False`.
3. Criar perfis:
   - `fast`;
   - `balanced`;
   - `quality`.
4. Testar combinações de `WHISPER_CPU_THREADS` e `WHISPER_NUM_WORKERS`.
5. Ajustar VAD para remover mais trechos sem fala quando fizer sentido.
6. Avaliar transcrição por chunks de `10-15min`.
7. Salvar chunks intermediários para permitir retomada.

## Métrica Que Deve Ser Registrada

```text
tempo_total_transcricao
duracao_audio
velocidade_realtime
segmentos_gerados
modelo
device
compute_type
beam_size
vad_filter
word_timestamps
```
