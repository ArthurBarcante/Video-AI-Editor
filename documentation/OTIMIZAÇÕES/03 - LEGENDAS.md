# 03 - Legendas

## Status Atual

- Tempo atual: `< 1s`
- Prioridade: Baixa para performance
- Processo base: `documentation/PROCESSOS/03 - LEGENDAS.md`

## Melhorias Concluídas

1. Pós-processamento específico para legenda.
   - Status: concluído.
   - Arquivo: `src/transcription/subtitle_cleaner.py`.
   - Remove hesitações iniciais, repetições excessivas e alongamentos simples sem alterar demais o significado.

2. Quebra inteligente de linhas.
   - Status: concluído.
   - Arquivo: `src/subtitles/line_breaker.py`.
   - Usa até 42 caracteres por linha, no máximo 2 linhas, com preferência por pontuação e conectores.

3. Melhor sincronização.
   - Status: concluído.
   - Tempo mínimo: `1s`.
   - Tempo máximo: `6s`.
   - Segmentos longos são divididos em blocos menores.

4. ASS separado para cada short.
   - Status: concluído.
   - Arquivo: `src/subtitles/short_subtitle_generator.py`.
   - Saída: `output/subtitles/short_01.ass`, `short_02.ass`, etc.
   - Os timestamps são ajustados para começar em `0s` dentro de cada short.

5. Segmentação específica para shorts.
   - Status: concluído.
   - Arquivo: `src/subtitles/subtitle_segmenter.py`.
   - Filtra segmentos por interseção com o corte.
   - Divide falas longas em até `5` palavras por legenda.
   - Limita cada legenda de short a aproximadamente `2.2s`.
   - Distribui o tempo proporcionalmente por palavra sem reativar `word_timestamps`.

6. Visual de ASS para shorts.
   - Status: concluído.
   - Fonte: `Montserrat ExtraBold`.
   - Tamanho: `70`.
   - Outline: `4`.
   - Shadow: `0`.
   - Alignment: `2`.

## Melhorias Pendentes

1. Usar word timestamps se o projeto decidir fazer karaoke real.
   - Prioridade: Baixa nesta fase.
   - Impacto: alto para estilo.
   - Risco: alto para performance da transcrição.

2. Integrar os `.ass` individuais diretamente no render final de cada short.
   - Prioridade: Alta para produto.
   - Impacto: alto para acabamento final.
   - Risco: médio, pois mexe nos comandos FFmpeg do render.

3. Criar estilos diferentes por tipo de short.
   - Prioridade: Média.
   - Impacto: médio/alto para identidade visual.
   - Risco: baixo/médio.
