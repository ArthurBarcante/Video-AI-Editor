# 03 - Legendas

## Objetivo

Gerar arquivos de legenda a partir do transcript para uso em vídeos longos, shorts e revisão manual.

## Onde Acontece

Arquivos principais:

```text
main.py
src/subtitles/srt_generator.py
src/subtitles/ass_generator.py
src/subtitles/line_breaker.py
src/subtitles/word_highlighter.py
src/utils/time_utils.py
```

## Entrada

```text
cache/transcripts/<nome>_transcript.json
```

## Saídas

```text
output/subtitles/<nome>_transcript.srt
output/subtitles/<nome>_transcript_short.ass
output/subtitles/<nome>_transcript_long.ass
```

## Como Atua Hoje

O `main.py` gera três arquivos:

1. SRT normal.
2. ASS modo `short`.
3. ASS modo `long`.

### SRT

O `generate_srt()`:

1. Carrega o transcript.
2. Valida o JSON com o schema `Transcript`.
3. Converte timestamps de segundos para formato SRT.
4. Escreve blocos numerados.

### ASS Short

O `generate_ass(mode="short")`:

1. Usa resolução base `1080x1920`.
2. Usa fonte maior.
3. Quebra linhas com limite menor.
4. Destaca palavras importantes com tags ASS.

Palavras destacadas hoje:

```text
mano
caraca
não acredito
meu deus
que isso
clipa
olha isso
```

### ASS Long

O `generate_ass(mode="long")`:

1. Usa fonte menor que shorts.
2. Mantém texto mais largo por linha.
3. Não aplica destaque de palavras.

## Cache

Usa cache por arquivo. Se a legenda já existe e `force=False`, a etapa é pulada.

## Tempo Observado

Na execução limpa, levou menos de `1s` para gerar SRT e ASS.

## Gargalos

Baixo impacto.

O custo é leitura do transcript e escrita de texto.

## Limitação Atual

As legendas são geradas para o transcript inteiro. Elas ainda não são separadas por corte individual. Isso aparece como fase futura no roadmap.

## Pontos De Otimização

Prioridade baixa para performance.

Melhorias futuras:

- Gerar `.ass` separado para cada short.
- Cortar timestamps da legenda por trecho renderizado.
- Melhorar layout visual dos estilos ASS.
- Usar word timestamps se o projeto decidir fazer karaoke real.
