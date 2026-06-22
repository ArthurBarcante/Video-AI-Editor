# 10 - Render dos Shorts

## Status Atual

- Tempo atual: `21.24s` com `SHORTS_RENDER_PROFILE=fast` e `2 workers`
- Referência anterior: `~1min09s`
- Tempo sequencial com perfil fast: `23.44s`
- Prioridade: Alta
- Processo base: `documentation/PROCESSOS/10 - RENDER DOS SHORTS.md`

## Já Feito

- Medição de tempo por short.
- Perfis de render.
- Render paralelo com limite de workers.

## Melhorias Pendentes

1. Gerar vertical direto do vídeo original para evitar reencode duplo.
   - Prioridade: Altíssima.
   - Impacto: muito alto.
   - Risco: médio/alto, muda arquitetura do pipeline.

2. Evitar `filter_complex` quando não houver SFX.
   - Prioridade: Alta.
   - Impacto: alto para shorts simples.
   - Risco: médio.

3. Só aplicar filtros quando necessário.
   - Prioridade: Alta.
   - Impacto: alto.
   - Risco: médio, corte com `-c copy` pode não ser preciso dependendo de keyframes.

4. Cache inteligente com assinatura do plano e das ações.
   - Prioridade: Alta.
   - Impacto: alto para confiabilidade.
   - Risco: médio.

5. Aplicar zoom temporal real com `enable='between(t,start,end)'`.
   - Prioridade: Média.
   - Impacto em qualidade: alto.
   - Impacto em performance: médio/negativo.
   - Risco: médio.

6. Melhorar posição do `-ss`.
   - Prioridade: Média.
   - Impacto: médio para qualidade/precisão.
   - Risco: baixo.

7. Otimizar SFX.
   - Prioridade: Média.
   - Impacto: médio.
   - Risco: baixo.
