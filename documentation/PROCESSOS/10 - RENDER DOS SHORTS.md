# 10 - Render Dos Shorts

## Objetivo

Renderizar os cortes curtos planejados no `edit_plan.json`, aplicando zoom e efeitos sonoros quando existirem ações automáticas.

## Onde Acontece

Arquivos principais:

```text
main.py
src/editing/shorts_builder.py
src/effects/zoom_effects.py
src/effects/sfx_effects.py
src/rendering/ffmpeg_utils.py
```

## Entrada

```text
cache/edit_plans/edit_plan.json
input/<video>.mp4
assets/sfx/*.mp3
```

## Saída

```text
output/shorts/short_01.mp4
output/shorts/short_02.mp4
output/shorts/short_03.mp4
output/shorts/short_04.mp4
output/shorts/short_05.mp4
```

## Como Atua Hoje

1. Carrega o `edit_plan.json`.
2. Lê `source_video`.
3. Itera pelos shorts planejados.
4. Para cada short:
   - define `start`;
   - define `duration`;
   - lê ações de zoom;
   - lê ações de SFX;
   - monta comando FFmpeg;
   - corta o trecho;
   - aplica o primeiro zoom encontrado;
   - mistura até 2 SFX;
   - exporta MP4 com `libx264` e `aac`.

## Ações Suportadas

### Zoom

O sistema aplica apenas o primeiro zoom do short.

Exemplo:

```json
{
  "type": "zoom",
  "intensity": 1.25,
  "target": "center",
  "reason": "zoom por alta intensidade"
}
```

### SFX

O sistema aplica no máximo 2 efeitos sonoros por short.

Exemplo:

```json
{
  "type": "sfx",
  "time": 731.3,
  "name": "impact",
  "volume": 0.35,
  "reason": "sfx por alta intensidade"
}
```

## Cache

Usa cache por short. Se `output/shorts/short_01.mp4` já existe e `force=False`, o short não é renderizado novamente.

## Tempo Observado

Na execução limpa:

```text
Shorts renderizados: 5
Tempo aproximado: ~1min09s
```

## Gargalos

Prioridade alta.

Motivos:

- Cada short chama FFmpeg separadamente.
- Os shorts são renderizados em sequência.
- O vídeo é reencodado com `libx264`.
- O short horizontal ainda será usado como entrada para a verticalização, gerando outro encode depois.

## Pontos De Otimização

Prioridade alta.

Melhorias futuras:

- Paralelizar render dos shorts.
- Usar preset FFmpeg mais rápido em modo teste.
- Gerar vertical direto do vídeo original para evitar reencode duplo.
- Aplicar zoom temporal real com `enable='between(t,start,end)'`.
- Evitar `filter_complex` quando não houver SFX.
- Medir tempo por short no log.
