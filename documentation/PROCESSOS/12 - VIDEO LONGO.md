# 12 - Vídeo Longo

## Objetivo

Gerar um vídeo compilado com os melhores segmentos da live, em ordem cronológica.

## Onde Acontece

Arquivos principais:

```text
main.py
src/editing/long_video_builder.py
src/planning/long_video_planner.py
src/rendering/ffmpeg_utils.py
```

## Entrada

```text
cache/edit_plans/edit_plan.json
input/<video>.mp4
```

## Saída

```text
output/long/video_01.mp4
```

## Como Atua Hoje

O planejamento do vídeo longo acontece antes, no `long_video_planner.py`.

Na renderização:

1. Carrega o `edit_plan.json`.
2. Lê os vídeos longos planejados.
3. Para cada vídeo longo:
   - cria uma pasta temporária;
   - corta cada segmento com FFmpeg;
   - salva cada segmento temporário;
   - cria um arquivo de concatenação;
   - concatena os segmentos com `-c copy`;
   - apaga os temporários;
   - salva o MP4 final.

## Corte De Segmentos

Cada segmento é cortado com:

```text
ffmpeg -y -ss <start> -i <video> -t <duration> -c:v libx264 -c:a aac <segment.mp4>
```

Depois os segmentos são concatenados com:

```text
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy output/long/video_01.mp4
```

## Cache

Usa cache por vídeo longo. Se `output/long/video_01.mp4` existe e `force=False`, a renderização é pulada.

## Tempo Observado

Na execução limpa:

```text
Vídeos longos renderizados: 1
Segmentos planejados: 6
Duração final planejada: ~113s
Tempo aproximado: ~2min27s
```

## Gargalos

Prioridade alta.

Motivos:

- Cada segmento é reencodado separadamente.
- O processo é sequencial.
- Segmentos temporários são escritos em disco.
- Para vídeos longos de `20-30min`, o custo será muito maior que no teste atual de `~113s`.

## Pontos De Otimização

Prioridade alta.

Melhorias futuras:

- Paralelizar corte dos segmentos.
- Usar corte por stream copy quando precisão permitir.
- Reduzir reencode desnecessário.
- Usar preset mais rápido em modo teste.
- Medir tempo por segmento.
- Criar estratégia diferente para vídeo longo de 20-30min.
