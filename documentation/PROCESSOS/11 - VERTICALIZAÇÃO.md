# 11 - Verticalização

## Objetivo

Converter os shorts renderizados para formato vertical `9:16`, adequado para Shorts, Reels e TikTok.

## Onde Acontece

Arquivos principais:

```text
main.py
src/rendering/verticalizer.py
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
3. Para cada short:
   - cria uma versão de fundo;
   - escala e corta o fundo;
   - aplica blur;
   - cria uma versão de frente preservando proporção;
   - centraliza a frente sobre o fundo;
   - exporta MP4 vertical.

## Layout Atual

```text
fundo blur 9:16
    +
vídeo original centralizado
```

Esse layout evita cortar informação importante do gameplay.

## Configuração Atual

```text
width=1080
height=1920
codec=libx264
preset=veryfast
audio=aac
```

## Cache

Usa cache por arquivo vertical. Se o vertical já existe e `force=False`, ele não é renderizado novamente.

## Tempo Observado

Na execução limpa:

```text
Shorts verticalizados: 5
Tempo aproximado: ~1min40s
```

## Gargalos

Prioridade alta.

Motivos:

- Cada verticalização reencoda o vídeo.
- A etapa roda depois do render horizontal, então há dois encodes para cada short.
- O blur de fundo aumenta custo de filtro.

## Pontos De Otimização

Prioridade alta.

Melhorias futuras:

- Renderizar o short vertical direto a partir do vídeo original.
- Paralelizar verticalização.
- Usar resolução menor em modo teste.
- Ajustar preset por perfil.
- Evitar blur pesado quando o modo for rápido.
- Medir tempo por arquivo vertical.
