# 01 - Extração De Áudio

## Objetivo

Separar o áudio do vídeo bruto em um formato simples para transcrição, highlights e análise emocional.

## Onde Acontece

Arquivos principais:

```text
main.py
src/audio/extractor.py
src/rendering/ffmpeg_utils.py
```

## Entrada

```text
input/live_bruta.mp4
```

## Saída

```text
cache/audio/<nome_do_video>.wav
```

Formato atual:

```text
WAV
pcm_s16le
mono
16 kHz
```

## Como Atua Hoje

1. Recebe o caminho do vídeo validado.
2. Define o caminho de saída em `cache/audio/`.
3. Se o `.wav` já existe e `force=False`, reaproveita o cache.
4. Se não existe, chama FFmpeg com:

```text
ffmpeg -y -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
```

5. Salva o áudio extraído.
6. Retorna o caminho do `.wav` para o pipeline.

## Quem Usa Esse Áudio

O mesmo arquivo é reutilizado por:

- transcrição;
- detecção de intensidade para highlights;
- análise de emoções;
- detecção simples de risada por variação de energia.

## Cache

Usa cache. Se o arquivo já existir, a extração é pulada.

## Tempo Observado

Na execução limpa com vídeo de `57min21s`, esta etapa levou poucos segundos.

Arquivo gerado:

```text
cache/audio/...wav
Tamanho: ~110 MB
```

Para uma live de `5-6h`, o WAV pode chegar perto de `600-700 MB`.

## Gargalos

Impacto médio.

Não foi o maior tempo da execução, mas gera arquivo grande e cria custo de disco. Esse arquivo também é lido novamente por outras etapas.

## Pontos De Otimização

Prioridade média.

Possíveis melhorias:

- Medir tempo exato de FFmpeg nesta etapa.
- Avaliar áudio intermediário comprimido, se não prejudicar Whisper e análises.
- Evitar releituras completas do WAV nas etapas seguintes.
- Criar extração por chunks para lives muito longas.
- Reaproveitar o mesmo áudio para transcrição e análise sem múltiplas leituras pesadas.
