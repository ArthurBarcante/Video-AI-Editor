# 00 - Validação do Vídeo

## Status Atual

- Tempo atual: `< 1s`
- Status: Funcionalmente concluído
- Prioridade: Baixa
- Processo base: `documentation/PROCESSOS/00 - VALIDAÇÃO DO VÍDEO.md`

## Já Feito

- Seleção explícita de arquivo por argumento posicional.
- Seleção explícita de arquivo via `--video`.
- Metadata de validação em `cache/metadata/`.

## Melhorias Pendentes

1. Aceitar outros formatos de entrada, como `.mkv`, `.mov` e `.webm`.
   - Prioridade: Média.
   - Impacto: médio para flexibilidade.
   - Risco: médio, depende de compatibilidade com FFmpeg e etapas seguintes.
   - Observação: fazer quando aparecer um arquivo real nesses formatos.

2. Avisar sobre resolução e FPS abaixo do recomendado.
   - Prioridade: Média.
   - Impacto: médio para evitar renders ruins.
   - Risco: baixo.
   - Observação: deve ser aviso, não bloqueio do pipeline.
