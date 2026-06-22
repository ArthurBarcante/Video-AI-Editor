# 11 - Verticalização

## Objetivo

Converter os shorts renderizados para formato vertical `9:16`, adequado para Shorts, Reels e TikTok.

## Onde Acontece

Arquivos principais:

```text
main.py
src/rendering/verticalizer.py
src/rendering/render_profiles.py
src/config/settings.py
src/rendering/ffmpeg_utils.py
```

## Entrada

```text
output/shorts/*.mp4
```

## Saída

```text
output/vertical/short_01_vertical.mp4
output/vertical/short_02_vertical.mp4
output/vertical/short_03_vertical.mp4
output/vertical/short_04_vertical.mp4
output/vertical/short_05_vertical.mp4
```

## Como Atua Hoje

1. Recebe a lista de shorts renderizados.
2. Ordena os caminhos.
3. Decide se usa resolução normal ou modo rápido.
4. Carrega o perfil de render.
5. Para cada short:
   - inicia medição de tempo;
   - monta o filtro vertical;
   - cria fundo blur se `VERTICAL_BLUR_ENABLED=true`;
   - centraliza o vídeo real sobre o fundo;
   - usa `-vf` com padding quando blur está desligado;
   - exporta MP4 vertical;
   - copia o áudio com `-c:a copy`;
   - registra o tempo individual.
6. Mede o tempo total da verticalização.

## Configuração Atual

```text
VERTICAL_WIDTH=1080
VERTICAL_HEIGHT=1920
VERTICAL_RENDER_PROFILE=fast
VERTICAL_RENDER_WORKERS=2
VERTICAL_RENDER_PARALLEL=true
VERTICAL_BLUR_ENABLED=true
VERTICAL_FAST_MODE=false
VERTICAL_FAST_WIDTH=540
VERTICAL_FAST_HEIGHT=960
```

O perfil `fast` vem de `src/rendering/render_profiles.py` e usa:

```json
{
  "video_codec": "libx264",
  "audio_codec": "aac",
  "preset": "veryfast",
  "crf": "28"
}
```

Na verticalização, o áudio é copiado com:

```text
-c:a copy
```

## Layout Atual

Com blur:

```text
fundo blur 9:16
    +
vídeo original centralizado
```

Sem blur:

```text
vídeo centralizado
    +
padding para preencher 9:16
```

## Modo Rápido

Quando `VERTICAL_FAST_MODE=true`, a saída usa:

```text
VERTICAL_FAST_WIDTH=540
VERTICAL_FAST_HEIGHT=960
```

Esse modo serve para desenvolvimento e validação rápida.

## Paralelismo

Quando `VERTICAL_RENDER_PARALLEL=true`, os shorts são verticalizados em paralelo com limite:

```text
min(VERTICAL_RENDER_WORKERS, quantidade_de_shorts)
```

O padrão atual usa `2` workers.

## Cache

Usa cache por arquivo vertical. Se o vertical já existe e `force=False`, ele não é renderizado novamente.

## Tempo Observado

Referência anterior:

```text
Shorts verticalizados: 5
Tempo aproximado: ~1min40s
```

Após esta otimização, o sistema registra:

```text
Vertical short_01.mp4 gerado em X.XXs usando perfil fast
Tempo total verticalização: X.XXs
```

Medições atuais no vídeo de teste:

```text
Blur ligado em 1080x1920: 114.24s
Blur desligado em 1080x1920: 40.61s
Modo rápido 540x960 com blur: 34.56s
```

Conclusão: medição, paralelismo, perfil, modo rápido e áudio copiado estão funcionando. O gargalo restante é o blur em resolução cheia.

## Gargalos

Prioridade alta.

Motivos:

- Cada verticalização ainda reencoda o vídeo.
- A etapa ainda roda depois do render horizontal.
- O blur de fundo aumenta custo quando ativado.
- Blur em 1080x1920 ainda está acima da referência anterior.

## Melhorias Concluídas

- Medir tempo por vertical. (**Feito**)
- Criar perfil de verticalização. (**Feito**)
- Paralelizar verticalização. (**Feito**)
- Blur configurável. (**Feito**)
- Modo rápido com resolução reduzida. (**Feito**)
- Evitar reencode de áudio usando `-c:a copy`. (**Feito**)

## Pontos De Otimização Pendentes

- Renderizar o short vertical direto a partir do vídeo original.
- Tornar o short horizontal opcional.
- Cache com assinatura.
- Otimizar o filtro de blur em resolução cheia.
