# 02 - Transcrição

## Status Atual

- Tempo atual: `279.31s` com `profile=fast` e `word_timestamps=false`
- Referência anterior: `~6min50s`
- Ganho observado: `~32%`
- Prioridade: Altíssima
- Processo base: `documentation/PROCESSOS/02 - TRANSCRIÇÃO.md`

## Já Feito

- `word_timestamps=false`.
- Métricas de performance da transcrição.
- Perfis de transcrição.
- Metadata no transcript.
- Transcrição por chunks.
- Cache parcial por chunk.
- Merge com timestamps globais.
- Métricas por chunk.
- VAD por perfil.
- Script de benchmark de workers/threads.
- Benchmark controlado de `WHISPER_CPU_THREADS` e `WHISPER_NUM_WORKERS`.
- Validação de chunking na live disponível de `57min21s`.
- Validação de retomada reaproveitando chunks parciais.

## Resultado Atual

- Melhor configuração observada: `WHISPER_CPU_THREADS=2` e `WHISPER_NUM_WORKERS=1`.
- Tempo em live de `57min21s`: `195.50s`.
- Velocidade realtime: `17.60x`.
- Chunks: `4` de até `900s`.
- Retomada com chunks em cache: `1.77s`.
- Timestamps inválidos: `0`.
- Regressões temporais: `0`.
- Relatório do benchmark: `cache/transcripts/benchmarks/benchmark_results.json`.

## Melhorias Pendentes

1. Validar chunking em live completa de `5-6h`.
   - Prioridade: Alta.
   - Impacto: alto para robustez e previsibilidade.
   - Risco: médio.
   - Observação: validado em live disponível de `57min21s`; falta arquivo bruto de `5-6h`.

2. Comparar `TRANSCRIPTION_CHUNKS_PARALLEL=true` com execução sequencial.
   - Prioridade: Média.
   - Impacto: médio/alto se o hardware aguentar.
   - Risco: médio, o modelo compartilhado e múltiplos chunks podem saturar CPU/RAM.

3. Comparar tempos entre perfis `fast`, `balanced` e `quality`.
   - Prioridade: Média.
   - Impacto: médio para qualidade.
   - Risco: baixo/médio.

4. Ajustar parâmetros de VAD por perfil com base em amostras reais.
   - Prioridade: Média.
   - Impacto: médio.
   - Risco: médio, VAD agressivo pode remover fala útil.

5. Evitar WAV gigante ou criar áudio otimizado para transcrição.
   - Prioridade: Média.
   - Impacto: médio em disco e I/O.
   - Risco: baixo/médio.
