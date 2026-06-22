# 11 - Verticalização

## Status Atual

- Tempo com blur em `1080x1920`: `114.24s`
- Tempo sem blur em `1080x1920`: `40.61s`
- Tempo em modo rápido `540x960` com blur: `34.56s`
- Prioridade: Alta
- Processo base: `documentation/PROCESSOS/11 - VERTICALIZAÇÃO.md`

## Já Feito

- Medição de tempo por vertical.
- Perfil de verticalização.
- Paralelização controlada.
- Blur configurável.
- Modo rápido com resolução reduzida.
- Áudio copiado com `-c:a copy`.

## Melhorias Pendentes

1. Renderizar o short vertical direto a partir do vídeo original.
   - Prioridade: Altíssima.
   - Impacto: muito alto.
   - Risco: médio/alto, junta responsabilidades do render horizontal e vertical.

2. Otimizar o filtro de blur em resolução cheia.
   - Prioridade: Alta.
   - Impacto: alto.
   - Risco: médio.

3. Tornar o short horizontal opcional.
   - Prioridade: Alta.
   - Impacto: alto.
   - Risco: médio.

4. Cache com assinatura.
   - Prioridade: Alta.
   - Impacto: alto para confiabilidade.
   - Risco: médio.
