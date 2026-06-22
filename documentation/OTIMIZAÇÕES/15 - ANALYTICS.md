# 15 - Analytics

## Status Atual

- Tempo atual: `< 1s`
- Prioridade: Alta para aprendizado real
- Processo base: `documentation/PROCESSOS/15 - ANALYTICS.md`

## Melhorias Concluídas

1. Criar camada `src/analytics/`.
   - Prioridade: Alta.
   - Impacto: alto.
   - Risco: baixo.

2. Importar métricas manuais por CSV.
   - Prioridade: Alta.
   - Impacto: alto porque evita depender de APIs no começo.
   - Risco: baixo.

3. Cruzar métricas com `edit_plan.json`.
   - Prioridade: Alta.
   - Impacto: alto para entender o que cada vídeo tinha.
   - Risco: médio, depende de `video_id` bater com o id do short.

4. Gerar relatório de performance.
   - Prioridade: Alta.
   - Impacto: alto para análise.
   - Risco: baixo.

5. Atualizar `learning_profile.json` com padrões reais.
   - Prioridade: Alta.
   - Impacto: alto.
   - Risco: médio, padrões ruins podem surgir com pouca amostra.

## Melhorias Pendentes

1. Criar comando dedicado para importar métricas.
   - Prioridade: Alta.
   - Impacto: alto para usabilidade.
   - Risco: baixo.

2. Exigir amostra mínima antes de alterar o perfil.
   - Prioridade: Alta.
   - Impacto: alto para evitar aprendizado precipitado.
   - Risco: baixo.

3. Aplicar duração ideal no planejamento de shorts.
   - Prioridade: Média/Alta.
   - Impacto: alto.
   - Risco: médio.

4. Aplicar padrões de título no gerador de títulos.
   - Prioridade: Média.
   - Impacto: médio/alto.
   - Risco: médio.

5. Integração com APIs de analytics.
   - Prioridade: Baixa nesta fase.
   - Impacto: alto.
   - Risco: alto por OAuth, permissões e limites de plataforma.
