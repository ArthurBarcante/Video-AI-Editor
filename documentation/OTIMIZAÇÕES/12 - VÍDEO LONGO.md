# 12 - Vídeo Longo

## Status Atual

- Tempo com perfil fast e `2 workers`: `42.50s` a `76.58s`
- Tempo sequencial com perfil fast: `46.65s`
- Prioridade: Alta
- Processo base: `documentation/PROCESSOS/12 - VIDEO LONGO.md`

## Já Feito

- Medição de tempo por segmento.
- Preset configurável.
- Paralelização controlada dos cortes.
- Cópia de áudio configurável.
- Relatório em `output/long/video_01.json`.

## Melhorias Pendentes

1. Usar corte por stream copy quando precisão permitir.
   - Prioridade: Altíssima.
   - Impacto: muito alto.
   - Risco: médio/alto, depende de keyframes e precisão de corte.

2. Criar estratégia diferente para vídeo longo de `20-30min`.
   - Prioridade: Alta.
   - Impacto: alto para o produto final.
   - Risco: médio/alto.

3. Reduzir reencode desnecessário.
   - Prioridade: Alta.
   - Impacto: alto.
   - Risco: médio.

4. Melhorar planejamento antes de renderizar.
   - Prioridade: Alta.
   - Impacto: alto para qualidade e tempo total.
   - Risco: médio.

5. Cache com assinatura do vídeo e do plano.
   - Prioridade: Alta.
   - Impacto: alto para confiabilidade.
   - Risco: médio.

6. Evitar temporários muito grandes.
   - Prioridade: Média.
   - Impacto: médio.
   - Risco: baixo/médio.
