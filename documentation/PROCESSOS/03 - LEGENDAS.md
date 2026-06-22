# 03 - Legendas

## Objetivo

Gerar arquivos de legenda a partir do transcript para uso em vídeos longos, shorts e revisão manual.

## Onde Acontece

Arquivos principais:

```text
main.py
src/subtitles/srt_generator.py
src/subtitles/ass_generator.py
src/subtitles/short_subtitle_generator.py
src/subtitles/subtitle_segmenter.py
src/subtitles/line_breaker.py
src/transcription/subtitle_cleaner.py
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
output/subtitles/short_01.ass
output/subtitles/short_02.ass
```

## Como Atua Hoje

O `main.py` gera três arquivos:

1. SRT normal.
2. ASS modo `short`.
3. ASS modo `long`.

Depois que o `edit_plan.json` existe, o sistema também gera uma legenda ASS individual para cada short planejado.

Antes de escrever as legendas globais, os segmentos passam por `subtitle_cleaner.py`:

1. Remove hesitações iniciais simples, como `é... é...`.
2. Colapsa repetições excessivas, como `mano mano mano`.
3. Normaliza alongamentos simples, como `ahhhhh`.
4. Aplica duração mínima de `1s`.
5. Divide legendas acima de `6s`.

### SRT

O `generate_srt()`:

1. Carrega o transcript.
2. Valida o JSON com o schema `Transcript`.
3. Limpa o texto dos segmentos.
4. Ajusta duração mínima e divide segmentos longos.
5. Converte timestamps de segundos para formato SRT.
6. Escreve blocos numerados.

### ASS Short

O `generate_ass(mode="short")`:

1. Usa resolução base `1080x1920`.
2. Usa fonte `Montserrat ExtraBold`.
3. Usa tamanho `70`, outline `4`, shadow `0` e alinhamento inferior central.
4. Quebra linhas com limite de até `42` caracteres e no máximo `2` linhas.
5. Não aplica karaoke, word timestamps ou destaque palavra por palavra.

### ASS Individual Por Short

O `generate_short_ass_files()`:

1. Lê o `edit_plan.json`.
2. Para cada short, filtra apenas segmentos que cruzam a janela do corte.
3. Corta os timestamps para o intervalo do short.
4. Recalcula os tempos para começar em `0s`.
5. Divide falas longas em blocos curtos.
6. Salva `output/subtitles/short_01.ass`, `short_02.ass`, etc.

A seleção e ajuste dos segmentos acontece em `subtitle_segmenter.py`.

Regras:

```text
segment.end > short.start
segment.start < short.end
```

Depois:

```text
new_start = max(0, segment.start - short.start)
new_end = min(short.duration, segment.end - short.start)
```

Para shorts, a divisão de legendas usa:

```text
máximo de 5 palavras por legenda
duração máxima de 2.2s por legenda
tempo distribuído proporcionalmente por palavra
```

Exemplo:

```text
short começa em 730.0s
fala original: 731.3 -> 733.5
fala no short: 1.3 -> 3.5
```

### ASS Long

O `generate_ass(mode="long")`:

1. Usa fonte menor que shorts.
2. Mantém texto mais largo por linha.
3. Usa o mesmo pós-processamento de texto e sincronização.

## Cache

Usa cache por arquivo. Se a legenda já existe e `force=False`, a etapa é pulada.

## Tempo Observado

Na execução limpa, levou menos de `1s` para gerar SRT e ASS.

## Gargalos

Baixo impacto.

O custo é leitura do transcript e escrita de texto.

## Pontos De Otimização

Prioridade baixa para performance.

Melhorias futuras:

- Integrar os `.ass` individuais diretamente no render final de cada short.
- Criar estilos diferentes por tipo de short.
- Usar word timestamps se o projeto decidir fazer karaoke real.
