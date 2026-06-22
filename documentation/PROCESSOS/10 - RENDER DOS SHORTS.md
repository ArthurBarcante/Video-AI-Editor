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
src/rendering/render_profiles.py
src/config/settings.py
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
   - carrega o perfil de render configurado;
   - inicia medição de tempo;
   - define `start`;
   - define `duration`;
   - lê ações de zoom;
   - lê ações de SFX;
   - monta comando FFmpeg;
   - corta o trecho;
   - aplica o primeiro zoom encontrado;
   - mistura até 2 SFX;
   - exporta MP4 com codec, preset e CRF do perfil;
   - registra o tempo de render do short.

O render pode rodar em modo sequencial ou paralelo controlado.

## Configuração Atual

```text
SHORTS_RENDER_PROFILE=fast
SHORTS_RENDER_WORKERS=2
SHORTS_RENDER_PARALLEL=true
```

## Perfis De Render

Arquivo:

```text
src/rendering/render_profiles.py
```

Perfis disponíveis:

```text
fast
balanced
quality
```

Perfil `fast`:

```json
{
  "video_codec": "libx264",
  "audio_codec": "aac",
  "preset": "veryfast",
  "crf": "28"
}
```

## Paralelismo

Quando `SHORTS_RENDER_PARALLEL=true`, o sistema usa `ThreadPoolExecutor` para renderizar shorts independentes em paralelo.

O número de workers é limitado por:

```text
min(SHORTS_RENDER_WORKERS, quantidade_de_shorts)
```

Com a configuração atual, o limite padrão é `2` workers.

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

Após esta otimização, o sistema registra:

```text
Short short_01 renderizado em X.XXs usando perfil fast
Tempo total render shorts: X.XXs
```

Meta realista com `SHORTS_RENDER_PROFILE=fast` e `SHORTS_RENDER_WORKERS=2`:

```text
5 shorts: ~35s a 50s
```

Resultado medido no vídeo atual:

```text
Referência anterior: ~1min09s
Perfil fast em paralelo com 2 workers: 21.24s
Perfil fast sequencial: 23.44s
```

Neste teste, o maior ganho veio do perfil `fast`. O paralelismo com 2 workers trouxe ganho pequeno, então ainda vale testar outros valores de workers antes de aumentar o padrão.

## Gargalos

Prioridade alta.

Motivos:

- Cada short ainda chama FFmpeg separadamente.
- Render paralelo usa mais CPU/disco.
- O vídeo é reencodado com `libx264`.
- O short horizontal ainda será usado como entrada para a verticalização, gerando outro encode depois.

## Pontos De Otimização

Prioridade alta.

Melhorias concluídas:

- Medir tempo por short. (**Feito**)
- Criar perfis de render. (**Feito**)
- Paralelizar render dos shorts com limite de workers. (**Feito**)

Melhorias futuras:

- Gerar vertical direto do vídeo original para evitar reencode duplo.
- Aplicar zoom temporal real com `enable='between(t,start,end)'`.
- Evitar `filter_complex` quando não houver SFX.
- Cache inteligente com assinatura do plano e das ações.
