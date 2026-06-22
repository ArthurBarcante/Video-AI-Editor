# 01 - Extração De Áudio

## Objetivo

Separar o áudio do vídeo bruto em um WAV padronizado para transcrição, highlights, emoções e análise de intensidade.

## Onde Acontece

Arquivos principais:

```text
main.py
src/audio/extractor.py
src/audio/audio_validator.py
src/audio/cache_signature.py
src/audio/chunker.py
src/config/settings.py
src/rendering/ffmpeg_utils.py
```

## Entrada

```text
input/<video>.mp4
```

## Saídas

```text
cache/audio/<nome_do_video>_<assinatura>.wav
cache/audio/<nome_do_video>_<assinatura>_audio_metadata.json
cache/audio/chunks/<nome_do_video>_<assinatura>/duration_900_overlap_2/
```

Exemplo de metadata:

```json
{
  "source_video": "input/live_bruta.mp4",
  "audio_path": "cache/audio/live_bruta_a1b2c3d4e5f6.wav",
  "cache_signature": "a1b2c3d4e5f6",
  "signature_strategy": "file_size_modified_time",
  "source_file_size_bytes": 1234567890,
  "source_modified_time_ns": 1760000000000000000,
  "execution_time_seconds": 8.42,
  "sample_rate": 16000,
  "channels": 1,
  "codec": "pcm_s16le",
  "file_size_bytes": 115000000,
  "fast_test_mode": false,
  "test_duration_seconds": null,
  "chunks_enabled": true,
  "chunks_metadata_path": "cache/audio/chunks/live_bruta_a1b2c3d4e5f6/duration_900_overlap_2/chunks_metadata.json",
  "chunk_count": 4,
  "chunk_duration": 900,
  "chunk_overlap": 2
}
```

## Como Atua Hoje

1. Recebe o vídeo validado.
2. Calcula uma assinatura rápida com `file_size + modified_time`.
3. Define o WAV em `cache/audio/` usando o nome `<stem>_<assinatura>.wav`.
4. Define o JSON de metadata ao lado do WAV.
5. Se o WAV assinado já existe e `force=False`, valida o arquivo existente e reaproveita o cache.
6. Se o WAV não existe, monta um comando FFmpeg.
7. Usa `-map 0:a:0` para selecionar explicitamente a primeira faixa de áudio.
8. Extrai áudio sem vídeo com `-vn`.
9. Aplica codec, sample rate e canais configurados no `.env`.
10. Mede o tempo real de execução.
11. Valida o WAV gerado com `ffprobe`.
12. Se `AUDIO_CREATE_CHUNKS=true`, cria chunks em `cache/audio/chunks/`.
13. Salva metadata da extração.
14. Retorna o caminho do WAV para o restante do pipeline.

## Comando Base

```text
ffmpeg -y -i input.mp4 -map 0:a:0 -vn -acodec pcm_s16le -ar 16000 -ac 1 cache/audio/audio_<assinatura>.wav
```

Em modo rápido de teste, o comando inclui:

```text
-t <AUDIO_TEST_DURATION>
```

## Configuração Atual

```text
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1
AUDIO_CODEC=pcm_s16le
AUDIO_TEST_DURATION=60
AUDIO_FAST_TEST_MODE=false
AUDIO_CREATE_CHUNKS=true
AUDIO_CHUNK_DURATION=900
AUDIO_CHUNK_OVERLAP=2
```

## Assinatura de Cache

A assinatura fica no nome do WAV e da metadata:

```text
<nome_do_video>_<assinatura>.wav
<nome_do_video>_<assinatura>_audio_metadata.json
```

Estratégia atual:

```text
sha256("<file_size>:<modified_time_ns>")[:12]
```

Isso é rápido e evita reutilização errada quando o conteúdo do vídeo muda, mas o nome permanece igual.

## Chunking Do Áudio

Quando `AUDIO_CREATE_CHUNKS=true`, a extração cria blocos WAV em:

```text
cache/audio/chunks/<nome_do_audio>/duration_<duracao>_overlap_<overlap>/
```

Exemplo:

```text
cache/audio/chunks/live_bruta_a1b2c3d4e5f6/duration_900_overlap_2/live_bruta_a1b2c3d4e5f6_chunk_001.wav
cache/audio/chunks/live_bruta_a1b2c3d4e5f6/duration_900_overlap_2/live_bruta_a1b2c3d4e5f6_chunk_002.wav
cache/audio/chunks/live_bruta_a1b2c3d4e5f6/duration_900_overlap_2/chunks_metadata.json
```

Esses chunks ajudam futuras etapas de transcrição por blocos, retomada de processamento e análise incremental em lives longas.

## Validação Do Áudio

O validador verifica:

- se o arquivo existe;
- se é arquivo, não pasta;
- se é `.wav`;
- se não está vazio;
- se o FFprobe encontra stream de áudio.

Arquivo:

```text
src/audio/audio_validator.py
```

## Cache

Usa cache por assinatura do vídeo.

Se o WAV assinado já existe, a etapa:

1. loga que o áudio está em cache;
2. valida o WAV;
3. cria ou reaproveita chunks de áudio, se habilitado;
4. retorna o caminho.

## Tempo Observado

Na execução limpa com vídeo de `57min21s`, a extração anterior levou `36.76s`.

A partir desta versão, o tempo exato passa a ser registrado em:

```text
cache/audio/<nome_do_video>_<assinatura>_audio_metadata.json
```

E nos logs:

```text
Tempo de extração: X.XXs
Tamanho do WAV: X.XX MB
```

## Melhorias Concluídas

1. Medir tempo real da extração. (**Feito**)
2. Usar `-map 0:a:0` explicitamente. (**Feito**)
3. Validar áudio extraído. (**Feito**)
4. Salvar metadata da extração. (**Feito**)
5. Criar modo rápido de teste. (**Feito**)
6. Cache com assinatura do vídeo. (**Feito**)
7. Chunking do áudio. (**Feito**)

## Gargalos

Prioridade média.

Motivos:

- A extração é rápida hoje, mas gera arquivos WAV grandes.
- Para lives de `5-6h`, o WAV pode chegar a centenas de MB.
- O mesmo WAV ainda pode ser lido por múltiplas etapas depois.

## Pontos De Otimização Pendentes

1. Evitar releitura completa do WAV usando `audio_features.json`.
2. Avaliar áudio separado por finalidade.
3. Validar se outro formato intermediário vale a pena.
