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
output/long/video_01.json
```

## Como Atua Hoje

O planejamento do vídeo longo acontece antes, no `long_video_planner.py`.

Na renderização:

1. Carrega o `edit_plan.json`.
2. Lê os vídeos longos planejados.
3. Para cada vídeo longo:
   - cria uma pasta temporária;
   - corta cada segmento com FFmpeg usando o perfil configurado;
   - mede o tempo de execução de cada corte;
   - salva cada segmento temporário;
   - pode cortar segmentos em paralelo;
   - cria um arquivo de concatenação;
   - concatena os segmentos com `-c copy`;
   - apaga os temporários;
   - salva o MP4 final;
   - gera um relatório JSON ao lado do vídeo final.

## Corte De Segmentos

Cada segmento é cortado com um comando nesta linha:

```text
ffmpeg -y -ss <start> -i <video> -t <duration> -c:v <codec> -preset <preset> -crf <crf> -c:a <audio> -movflags +faststart <segment.mp4>
```

O codec, preset e CRF vêm do perfil definido em `LONG_RENDER_PROFILE`.

Perfis atuais:

```text
fast: libx264, veryfast, crf 28
balanced: libx264, fast, crf 23
quality: libx264, medium, crf 20
```

O áudio usa `aac` por padrão. Quando `LONG_AUDIO_COPY=true`, o áudio é copiado com `-c:a copy`.

Depois os segmentos são concatenados com:

```text
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy output/long/video_01.mp4
```

## Paralelismo

O corte dos segmentos pode rodar em paralelo.

Configurações:

```text
LONG_RENDER_PARALLEL=true
LONG_RENDER_WORKERS=2
```

Com paralelismo ligado, o sistema limita a quantidade de workers ao menor valor entre `LONG_RENDER_WORKERS` e a quantidade de segmentos planejados.

## Relatório

Depois de exportar o vídeo longo, o sistema gera:

```text
output/long/video_01.json
```

O relatório registra:

- ID do vídeo longo.
- Caminho do MP4 final.
- Quantidade de segmentos.
- Duração planejada.
- Tempo total de exportação.
- Perfil de render usado.
- Se o render foi paralelo.
- Quantidade de workers.
- Se o áudio foi copiado.
- Tempo de corte de cada segmento.

Exemplo:

```json
{
  "id": "video_01",
  "output_path": "output/long/video_01.mp4",
  "segment_count": 6,
  "planned_duration": 113.0,
  "total_execution_time_seconds": 38.5,
  "render_profile": "fast",
  "parallel": true,
  "workers": 2,
  "audio_copy": false,
  "segments": [
    {
      "id": "segment_001",
      "start": 112.5,
      "end": 134.2,
      "duration": 21.7,
      "execution_time_seconds": 12.4
    }
  ]
}
```

## Cache

Usa cache por vídeo longo. Se `output/long/video_01.mp4` existe e `force=False`, a renderização é pulada.

## Tempo Observado

Na execução limpa:

```text
Vídeos longos renderizados: 1
Segmentos planejados: 6
Duração final planejada: ~113s
Tempo anterior aproximado: ~2min27s
Tempo atual com perfil fast e 2 workers: 42.50s a 76.58s
Tempo atual sequencial com perfil fast: 46.65s
```

Conclusão da medição: o paralelismo controlado pode reduzir o tempo, mas oscila bastante nesta máquina porque múltiplos FFmpeg competem por CPU e disco. O processo ficou configurável e observável. O próximo gargalo grande continua sendo reencodar cada segmento em vez de usar uma estratégia segura de stream copy de vídeo.

## Gargalos

Prioridade alta.

Motivos:

- Cada segmento é reencodado separadamente.
- Mesmo com paralelismo, múltiplos FFmpeg podem saturar CPU e disco.
- Segmentos temporários são escritos em disco.
- Para vídeos longos de `20-30min`, o custo será muito maior que no teste atual de `~113s`.

## Pontos De Otimização

Prioridade alta.

Melhorias futuras:

- Usar corte por stream copy quando precisão permitir.
- Reduzir reencode desnecessário.
- Criar estratégia diferente para vídeo longo de 20-30min.
- Evitar temporários muito grandes.
- Criar cache com assinatura do vídeo e do plano.
