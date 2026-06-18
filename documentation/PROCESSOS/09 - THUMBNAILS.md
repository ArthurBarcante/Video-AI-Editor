# 09 - Thumbnails

## Objetivo

Gerar miniaturas automaticamente para cada short e para o vídeo longo.

## Onde Acontece

Arquivos principais:

```text
main.py
src/thumbnails/thumbnail_generator.py
src/thumbnails/frame_capture.py
src/thumbnails/thumbnail_selector.py
```

## Entrada

```text
cache/edit_plans/edit_plan.json
input/<video>.mp4
```

## Saídas

```text
output/thumbnails/short_01.jpg
output/thumbnails/short_02.jpg
output/thumbnails/video_01.jpg
output/thumbnails/frames/short_01_frame.jpg
output/thumbnails/frames/video_01_frame.jpg
```

## Como Atua Hoje

1. Carrega o plano de edição.
2. Para cada short:
   - calcula o timestamp central do corte;
   - captura um frame do vídeo original;
   - aplica texto com Pillow;
   - salva a thumbnail final.
3. Para cada vídeo longo:
   - usa o primeiro segmento;
   - captura um frame no meio desse segmento;
   - aplica o título do vídeo;
   - salva a thumbnail final.

## Captura De Frame

A captura usa FFmpeg:

```text
ffmpeg -y -ss <timestamp> -i <video> -frames:v 1 -q:v 2 <frame.jpg>
```

Se a captura falha ou gera arquivo vazio, o sistema tenta capturar o frame em `0s`.

## Template Atual

O template é simples:

- converte imagem para RGB;
- usa fonte `DejaVuSans-Bold.ttf` ou `Arial.ttf`;
- coloca texto em caixa alta;
- limita o texto a `32` caracteres;
- desenha uma caixa preta;
- escreve texto branco.

## Cache

Usa cache por thumbnail. Se a imagem final existe e `force=False`, ela é reaproveitada.

## Tempo Observado

Na execução limpa:

```text
Thumbnails geradas: 6
Tempo aproximado: ~3s
```

## Gargalos

Baixo impacto no cenário atual.

Pode crescer se houver muitos shorts, porque cada thumbnail chama FFmpeg separadamente.

## Pontos De Otimização

Prioridade baixa para performance.

Melhorias futuras:

- Paralelizar capturas de frame.
- Selecionar frames com mais movimento ou rosto.
- Usar templates por tipo de conteúdo.
- Usar título escolhido em `titles.json`, não apenas o título do plano.
- Criar thumbnails diferentes por plataforma.
