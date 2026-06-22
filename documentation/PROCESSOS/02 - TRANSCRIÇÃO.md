# 02 - Transcrição

## Objetivo

Converter o áudio da live em texto com timestamps para que o restante do sistema consiga analisar falas, gerar legendas, detectar highlights e planejar cortes.

## Onde Acontece

Arquivos principais:

```text
main.py
src/transcription/whisper_transcriber.py
src/transcription/chunking.py
src/transcription/chunk_transcriber.py
src/transcription/chunk_merger.py
src/transcription/text_cleaner.py
src/transcription/transcript_schema.py
src/transcription/transcription_profiles.py
src/config/settings.py
```

## Entrada

```text
cache/audio/<nome_do_video>.wav
```

## Saída

```text
cache/transcripts/<nome_do_audio>_transcript.json
cache/transcripts/chunks/<nome_do_audio>/duration_900_overlap_2/chunk_001.wav
cache/transcripts/chunks/<nome_do_audio>/duration_900_overlap_2/chunk_001.json
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
  ],
  "metadata": {
    "execution_time_seconds": 279.31,
    "audio_duration_seconds": 3441.1973125,
    "realtime_speed": 12.32,
    "segment_count": 1241,
    "model": "tiny",
    "device": "cpu",
    "compute_type": "int8",
    "beam_size": 1,
    "best_of": 1,
    "vad_filter": true,
    "word_timestamps": false,
    "profile": "fast",
    "chunking_enabled": true,
    "chunk_duration": 900,
    "chunk_overlap": 2,
    "chunk_count": 4,
    "chunks_reused_from_cache": 2,
    "chunk_metrics": [
      {
        "index": 1,
        "chunk_audio": "cache/transcripts/chunks/live/duration_900_overlap_2/chunk_001.wav",
        "chunk_start_offset": 0.0,
        "duration": 900.0,
        "execution_time_seconds": 62.4,
        "segment_count": 320,
        "reused_from_cache": false
      }
    ]
  }
}
```

## Como Atua Hoje

1. Valida se o arquivo de áudio existe, é `.wav` e não está vazio.
2. Define a saída em `cache/transcripts/`.
3. Se o transcript já existe e `force=False`, reaproveita o cache.
4. Se `TRANSCRIPTION_USE_CHUNKS=true`, calcula blocos de áudio.
5. Cria ou reaproveita WAVs em `cache/transcripts/chunks/<nome_do_audio>/`.
6. Carrega o `faster-whisper` uma vez.
7. Transcreve cada chunk e salva um JSON parcial por chunk.
8. Converte os timestamps locais do chunk para timestamps globais da live.
9. Junta os segmentos com `merge_chunk_segments()`.
10. Remove duplicatas simples geradas pela sobreposição entre chunks.
11. Salva o JSON final com metadata global e métricas por chunk.

Se `TRANSCRIPTION_USE_CHUNKS=false`, o sistema usa a transcrição cheia em um único `model.transcribe()`.

## Configuração Atual

```text
WHISPER_MODEL=tiny
WHISPER_LANGUAGE=pt
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
WHISPER_CPU_THREADS=2
WHISPER_NUM_WORKERS=1
WHISPER_BEAM_SIZE=0
WHISPER_BEST_OF=0
WHISPER_VAD_FILTER=true
WHISPER_CONDITION_ON_PREVIOUS_TEXT=false
WHISPER_WORD_TIMESTAMPS=false
WHISPER_PROFILE=fast
TRANSCRIPTION_USE_CHUNKS=true
TRANSCRIPTION_CHUNK_DURATION=900
TRANSCRIPTION_CHUNK_OVERLAP=2
TRANSCRIPTION_CHUNK_WORKERS=1
TRANSCRIPTION_CHUNKS_PARALLEL=false
```

Quando `WHISPER_BEAM_SIZE=0` ou `WHISPER_BEST_OF=0`, o sistema usa os valores definidos pelo perfil selecionado.

## Perfis Atuais

Os perfis ficam em:

```text
src/transcription/transcription_profiles.py
```

Perfis disponíveis:

```text
fast
balanced
quality
```

O perfil `fast` usa `beam_size=1`, `best_of=1`, `word_timestamps=false`, `condition_on_previous_text=false`, `vad_filter=true` e `vad_parameters.min_silence_duration_ms=500`.

Os perfis também definem parâmetros iniciais de VAD:

```text
fast: min_silence_duration_ms=500
balanced: min_silence_duration_ms=700
quality: min_silence_duration_ms=1000
```

## Metadata De Performance

O transcript salva uma seção `metadata` com:

```text
tempo de execução
duração do áudio
velocidade realtime
quantidade de segmentos
modelo
device
compute type
beam size
best of
VAD
word timestamps
perfil
chunking habilitado
duração do chunk
overlap do chunk
quantidade de chunks
chunks reaproveitados do cache
métricas por chunk
```

Essa metadata é a base para comparar otimizações.

## Cache

Usa dois níveis de cache:

1. Cache final: se `cache/transcripts/<nome>_transcript.json` existe e `force=False`, a transcrição inteira é pulada.
2. Cache parcial: se o transcript final não existe, mas os JSONs dos chunks existem, cada chunk já transcrito é reaproveitado.

Isso permite retomar transcrições longas sem perder todo o trabalho caso a execução seja interrompida.

## Tempo Observado

Na execução limpa com vídeo de `57min21s`:

```text
Tempo anterior de referência: ~6min50s
Tempo após word_timestamps=false: 279.31s
Tempo após chunking e benchmark CPU/worker: 195.50s
Duração do áudio: 3441.20s
Velocidade realtime: 17.60x
Segmentos gerados: 1178
Perfil usado: fast
word_timestamps: false
Chunks: 4 de até 900s
Chunks reutilizados do cache na primeira execução: 0
Ganho aproximado contra referência inicial: ~52%
```

Ainda é uma das etapas mais importantes do pipeline, mas a combinação de `word_timestamps=false`, chunking e ajuste de CPU/worker reduziu significativamente o tempo.

Validação curta da camada de chunks:

```text
Áudio sintético: 3s
Chunk duration: 1s
Chunks gerados: 3
Primeira execução: 1.62s
Segunda execução reaproveitando chunks: 0.95s
Chunks reutilizados do cache: 3
```

Validação na live disponível do projeto:

```text
Arquivo: cache/audio/Vi o ICEBERG da CALVOESFERA...
Duração: 57min21s
Chunk duration: 900s
Chunk overlap: 2s
Chunks: 4
Tempo limpo: 195.50s
Realtime speed: 17.60x
Segmentos: 1178
Timestamps inválidos: 0
Regressões temporais: 0
Último segmento: 3441.19s
```

Validação de retomada:

```text
Transcript final removido
Chunks parciais mantidos
Chunks reutilizados: 4
Tempo para reconstruir transcript final: 1.77s
```

Benchmark de `WHISPER_CPU_THREADS` e `WHISPER_NUM_WORKERS` com chunks de `300s`:

```text
cpu_threads | num_workers | tempo   | realtime | segmentos | RAM máx
0           | 1           | 217.84s | 15.80x   | 1055      | 591240 KB
0           | 2           | 278.18s | 12.37x   | 1055      | 622000 KB
0           | 4           | 276.81s | 12.43x   | 1055      | 709560 KB
2           | 1           | 201.21s | 17.10x   | 1055      | 602092 KB
2           | 2           | 207.99s | 16.54x   | 1055      | 642892 KB
2           | 4           | 226.64s | 15.18x   | 1055      | 717004 KB
4           | 1           | 287.52s | 11.97x   | 1055      | 591280 KB
4           | 2           | 284.62s | 12.09x   | 1055      | 644468 KB
4           | 4           | 320.80s | 10.73x   | 1055      | 722180 KB
```

Melhor resultado observado: `WHISPER_CPU_THREADS=2` e `WHISPER_NUM_WORKERS=1`.

Relatório do benchmark:

```text
cache/transcripts/benchmarks/benchmark_results.json
```

## Gargalos

Prioridade altíssima.

Motivos:

- A transcrição escala com a duração do vídeo.
- Para lives de `5-6h`, ainda pode ser um dos maiores custos se escalar de forma linear.
- O processo agora tem cache parcial por chunk, validado na live disponível de `57min21s`.
- Ainda falta validar em live real de `5-6h`.
- Chunking paralelo existe como configuração, mas fica desligado por padrão até validação de estabilidade.

## Pontos De Otimização

Prioridade sugerida:

1. Desativar `word_timestamps` por padrão. (**Feito**)
2. Salvar metadata de performance no transcript. (**Feito**)
3. Criar perfis `fast`, `balanced` e `quality`. (**Feito**)
4. Implementar transcrição por chunks. (**Feito**)
5. Salvar chunks intermediários para permitir retomada. (**Feito**)
6. Juntar chunks com timestamps globais. (**Feito**)
7. Salvar métricas por chunk. (**Feito**)
8. Adicionar VAD por perfil. (**Feito**)
9. Criar script de benchmark de workers/threads. (**Feito**)
10. Executar benchmark real de `WHISPER_CPU_THREADS` e `WHISPER_NUM_WORKERS`. (**Feito**)
11. Validar retomada com cache parcial. (**Feito**)
12. Comparar tempos entre `fast`, `balanced` e `quality`.
13. Validar em live real de `5-6h`.

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
best_of
vad_filter
word_timestamps
profile
chunking_enabled
chunk_duration
chunk_overlap
chunk_count
chunks_reused_from_cache
chunk_metrics
```
