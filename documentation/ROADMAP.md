# ROADMAP

Este documento descreve a evolução planejada do projeto Video AI Editor.

O objetivo do projeto é construir uma plataforma capaz de transformar automaticamente uma live bruta em múltiplos conteúdos prontos para publicação utilizando inteligência artificial.

---

# Visão de Longo Prazo

Receber um vídeo bruto de várias horas e gerar automaticamente:

* Shorts para YouTube Shorts.
* Vídeos para TikTok.
* Vídeos para Instagram Reels.
* Vídeos longos para YouTube.
* Legendas.
* Zooms.
* Efeitos sonoros.
* Títulos.
* Descrições.
* Thumbnails.
* Conteúdo pronto para publicação.

O objetivo final é que a IA execute tarefas normalmente realizadas por um editor humano.

---

# Fase 1 — Fundação

Status: **Concluída**
Objetivo:

Criar a base sólida do projeto.

## Entregas

* Estrutura de diretórios. (**Feito**)
* Organização modular do código. (**Feito**)
* Configurações centralizadas. (**Feito**)
* Sistema de logs. (**Feito**)
* Sistema de cache. (**Feito**)
* Estrutura de documentação. (**Feito**)
* Ambiente de desenvolvimento. (**Feito**)

## Resultado Esperado

Projeto organizado, documentado, configurável e preparado para crescer com cache, logs e diretórios padronizados.

---

# Fase 2 — Processamento de Vídeo

Status: **Concluída**

Objetivo:

Permitir leitura e manipulação de vídeos.

## Entregas

* Leitura de arquivos MP4. (**Feito**)
* Extração de áudio. (**Feito**)
* Validação de vídeo. (**Feito**)
* Obtenção de metadados. (**Feito**)
* Conversões básicas com FFmpeg. (**Feito**)

## Resultado Esperado

O sistema consegue localizar, validar e preparar vídeos MP4 com áudio para as próximas etapas de análise.

---

# Fase 3 — Transcrição

Status: **Concluída**

Objetivo:

Converter fala em texto.

## Entregas

* Integração com Whisper. (**Feito**)
* Geração de transcript.json. (**Feito**)
* Geração de SRT. (**Feito**)
* Geração de ASS. (**Feito**)
* Sistema de timestamps. (**Feito**)

## Resultado Esperado

O conteúdo falado fica disponível em `transcript.json`, com timestamps reutilizáveis para legendas, análise e highlights.

---

# Fase 4 — Sistema de Highlights

Status: **Concluída**

Objetivo:

Detectar automaticamente momentos interessantes.

## Entregas

* Detector de palavras-chave. (**Feito**)
* Detector de intensidade de fala. (**Feito**)
* Detector de exclamações. (**Feito**)
* Detector de risadas. (**Feito**)
* Sistema de score. (**Feito**)
* highlights.json. (**Feito**)
* Perfil rápido para lives de 5 a 6 horas. (**Feito**)
* Cache respeitado nas etapas até highlights. (**Feito**)
* Leitura de intensidade sem carregar o WAV inteiro. (**Feito**)

## Meta de Performance

Executar as fases 1 a 4 em 15 a 20 minutos para lives de 5 a 6 horas usando perfil rápido, cache ativo, modelo Whisper leve e leitura de áudio por segmento.

## Resultado Esperado

O sistema gera `cache/highlights/highlights.json` com candidatos a melhores momentos, pontuação e motivos de seleção.

---

# Fase 5 — Planejamento de Edição

Status: **Concluída**

Objetivo:

Separar análise de renderização.

## Entregas

* edit_plan.json. (**Feito**)
* Sistema de decisões. (**Feito**)
* Planejamento de shorts. (**Feito**)
* Planejamento de vídeos longos. (**Feito**)
* Priorização de highlights. (**Feito**)

## Resultado Esperado

O sistema gera `cache/edit_plans/edit_plan.json` com shorts, vídeo longo planejado, segmentos priorizados e ações preparadas para renderização futura.

---

# Fase 6 — Geração de Shorts

Status: **Concluída**

Objetivo:

Criar vídeos curtos automaticamente.

## Entregas

* Seleção automática de trechos. (**Feito**)
* Shorts de 15 a 45 segundos. (**Feito**)
* Renderização automática. (**Feito**)
* Exportação em MP4. (**Feito**)

## Resultado Esperado

O sistema renderiza os shorts planejados em `output/shorts/` como arquivos MP4.

---

# Fase 7 — Geração de Vídeos Longos

Status: **Concluída**

Objetivo:

Montar vídeos completos utilizando os melhores momentos.

## Entregas

* Agrupamento de highlights. (**Feito**)
* Organização narrativa. (**Feito**)
* Criação de vídeos entre 20 e 30 minutos. (**Feito**)
* Renderização automática. (**Feito**)

## Resultado Esperado

O sistema renderiza os vídeos longos planejados em `output/long/` como arquivos MP4.

---

# Fase 8 — Legendas Inteligentes

Status: **Concluído**

Objetivo:

Melhorar a experiência visual.

## Entregas

* Estilos dinâmicos. (**Feito**)
* Destaque de palavras. (**Feito**)
* Quebra inteligente de linhas. (**Feito**)
* Legendas para Shorts. (**Feito**)
* Legendas para vídeos longos. (**Feito**)

## Resultado Esperado

Conteúdo mais profissional e mais fácil de consumir.

---

# Fase 9 — Zooms Automáticos

Status: **Concluído**

Objetivo:

Destacar momentos importantes.

## Entregas

* Zoom baseado em eventos. (**Feito**)
* Zoom baseado em palavras-chave. (**Feito**)
* Zoom baseado em emoção. (**Feito**)
* Configuração de intensidade. (**Feito**)

## Resultado Esperado

Vídeos mais dinâmicos sem edição manual.

---

# Fase 10 — Efeitos Sonoros

Status: **Concluído**

Objetivo:

Adicionar impacto à edição.

## Entregas

* Biblioteca de SFX. (**Feito**)
* Aplicação automática. (**Feito**)
* Regras de uso. (**Feito**)
* Controle de frequência. (**Feito**)

## Resultado Esperado

Conteúdo mais envolvente.

---

# Fase 11 — Verticalização Inteligente

Status: **Concluído**

Objetivo:

Criar versões para Shorts e Reels.

## Entregas

* Conversão automática para 9:16. (**Feito**)
* Crop automático simples. (**Feito**)
* Blur de fundo. (**Feito**)
* Layout adaptativo básico. (**Feito**)

## Resultado Esperado

Conteúdo otimizado para dispositivos móveis.

---

# Fase 12 — IA de Contexto

Status: **Concluído**

Objetivo:

Entender o conteúdo além das palavras.

## Entregas

* Análise semântica. (**Feito**)
* Entendimento de contexto. (**Feito**)
* Agrupamento por assunto. (**Feito**)
* Identificação de momentos importantes. (**Feito**)

## Resultado Esperado

Highlights mais inteligentes.

---

# Fase 13 — IA de Emoção

Status: **Concluído**

Objetivo:

Reconhecer intensidade emocional.

## Entregas

* Detecção de surpresa. (**Feito**)
* Detecção de raiva. (**Feito**)
* Detecção de alegria. (**Feito**)
* Detecção de empolgação. (**Feito**)

## Resultado Esperado

Melhor seleção de momentos virais.

---

# Fase 14 — Títulos Automáticos

Status: **Concluído**

Objetivo:

Criar títulos atrativos.

## Entregas

* Geração automática de títulos. (**Feito**)
* Múltiplas sugestões. (**Feito**)
* Otimização para CTR. (**Feito**)

## Resultado Esperado

Maior potencial de alcance.

---

# Fase 15 — Geração de Thumbnails

Status: **Concluído**

Objetivo:

Automatizar a criação de miniaturas.

## Entregas

* Captura de frames. (**Feito**)
* Seleção de melhores imagens. (**Feito**)
* Inserção de texto. (**Feito**)
* Templates. (**Feito**)

## Resultado Esperado

Pipeline completo de produção.

---

# Fase 16 — Publicação Automática

Status: **Desenvolvimento**
Objetivo:

Eliminar etapas manuais.

## Entregas

* Plano seguro de publicação. (**Feito**)
* Integração com YouTube. ()
* Integração com TikTok. ()
* Integração com Instagram. ()
* Agendamento de publicações. ()

## Resultado Esperado

Conteúdo preparado para publicação automática, com upload real pendente de OAuth, permissões e revisão de app.

---

# Processos do Sistema

## Validação do vídeo
- Tempo de Execução atual: < 1s
### Otimizações e Melhorias
- Prioridade: Baixa

## Extração de Áudio
- Tempo de Execução Atual: < 30s
### Otimizações e Melhorias
- Prioridade: Média
- 1. Medir tempo real da extração
  - Impacto: alto para diagnóstico
  - Risco: baixo
- 2. Validar se WAV PCM ainda é o melhor formato intermediário
  - Impacto: médio
  - Risco: médio, análise de energia atual espera WAV
- 3. Criar áudio separado por finalidade
  - Impacto: baixo/médio
  - Risco: médio
- 4. Evitar releitura pesada do áudio em etapas seguintes
  - Impacto: alto para análise de áudio em lives longas
  - Risco médio
- 5. Chunking do áudio
  - Impacto: alto para robustez futura
  - Risco: médio
- 6. Usar -map explicitamente
  - Impacto: baixo para performace, médio para confiabilidade
  - Risco: baixo
- 7. Adicionar validação do áudio extraído
  - Impacto: médio para confiabilidade
  - Risco: baixo
- 8. Criar modo rápido de teste
  - Impacto: alto em desenvolvimento
  - Risco: baixo se limitado ao modo dev/test
- 9. Cache com assinatura do vídeo
  - Impacto: alto para segurança do cache
  - Risco: médio, mexe em nomes e dependências

## Transcrição
- Tempo de Execução Atual: ~6min50s
### Otimizações e Melhorias
- Prioridade: Altíssima
- 1. Desativar word_timestamps=True
  - Impacto: alto
  - Risco: baixo
- 2. Adicionar métricas de performance da trasncrição
  - Impacto: alto para decisão técnica
  - Risco: baixo
- 3. Criar perfis de transcrição
  - Impacto: médio/alto
  - Risco: baixo/médio
- 4. Testar WHISPER_CPU_THREADS e WHISPER_NUM_WORKERS
  - Impacto: médio
  - Risco: baixo
- 5. Ajustar VAD
  - Impacto: médio, dependendo da live
  - Risco: médio, VAD agressivo pode remover fala útilo
- 6. Transcrição por chunks
  - Impacto: alto para robustez
  - Impacto em velocidade: médio inicialmente, alto se paralelizar
  - Risco: médio, ajuste de timestamps e junção de chunks
- 7. Evitar WAV gigante ou criar áudio otimizado para transcrição
  - Impacto: médio em disco/I/O
  - Risco: baixo/médio
- 8. Salvar metadados da trasncrição
  - Impacto: alto para análise
  - Risco: baixo

## Legendas
- Tempo de Execução Atual: < 1s
### Otimizações e Melhorias
- Prioridade: Baixa

## Highlights
- Tempo de Execução Atual: < 1s
### Otimizações e Melhorias
- Prioridade: Baixa

## Contexto
- Tempo de Execução Atual: < 1s
### Otimizações e Melhorias
- Prioridade: Baixa

## Emoções
- Tempo de Execução Atual: < 1s
### Otimizações e Melhorias
- Prioridade: Baixa

## Plano de Edição
- Tempo de Execução Atual: < 1s
### Otimizações e Melhorias
- Prioridade: Baixa

## Títulos
- Tempo de Execução Atual: < 1s
### Otimizações e Melhorias
- Prioridade: Baixa

## Thumbnails
-  Tempo de Execução Atual: ~3s
### Otimizações e Melhorias
- Prioridade: Baixa

## Render dos Shorts
- Tempo de Execução Atual: ~1min09s
### Otimizações e Melhorias
- Prioridade: Alta
- 1. Medir tempo por short
  - Impacto: alto para diagnóstico
  - Risco: baixo
- 2. Paralelizar render dos shorts
  - Impacto: alto
  - Risco: médio, uso intenso de CPU/disco
- 3. Criar preset de render por perfil
  - Impacto: alto
  - Risco: baixo/médio, pode alterar qualidade/tamanho
- 4. Gerar vertical direto no vídeo original
  - Impacto: muito alto
  - Risco: médio/alto, muda arquitetura do pipeline
- 5. Só aplicar filtros quando necessário
  - Impacto: alto para shorts simples
  - Risco: médio, corte com -c copy pode não ser preciso dependendo de keyframes
- 6. Melhorar posição do -ss
  - Impacto: médio para qualidade/precisão
  - Risco: baixo
- 7. Otimizar SFX
  - Impacto: médio
  - Risco: baixo
- 8. Zoom temporal real
  - Impacto em qualidade: alto
  - Impacto em performance: médio/negativo
  - Risco: médio
- Cache mais inteligente
  - Impacto: alto para confiabilidade
  - Risco: médio

## Verticalização
- Tempo de Execução Atual: ~1min40s
### Otimizações e Melhorias
- Prioridade: Alta
- 1. Medir tempo por vertical
  - Impacto: alto para diagnóstico
  - Risco: baixo
- 2. Paralelizar verticalização
  - Impacto: alto
  - Risco: médio, FFmpeg em paralelo pode saturar CPU
- 3. Gerar vertical direto do vídeo original
  - Impacto: muito alto
  - Risco: médio/alto, junta responsabilidade shorts_builder e verticalizer
- 4. Tornar o short horizontal opcional
  - Impacto: alto
  - Risco: médio
- 5. Modo rápido com resolução reduzida
  - Impacto: alto em desenvolvimento
  - Risco: baixo
- 6. Blur configurável
  - Impacto: médio/alto
  - Risco: baixo/médio, muda estética
- 7. Usar preset configurável
  - Impacto: médio
  - Risco: baixo
- 8. Evitar reencode de áudio
  - Impacto: baixo/médio
  - Risco: baixo, desde que o áudio de entrada seja compatível
- 9. Cache com assinatura
  - Impacto: alto para confiabilidade
  - Risco: médio

## Video Longo
- Tempo de Execução Atual: ~2min27s
### Otimizações e Melhorias
- Prioridade: Alta

## Plano de Publicação
- Tempo de Execução Atual: < 1s
### Otimizações e Melhorias
- Prioridade: Baixa
- 1. Medir tempo por segmento
  - Impacto: alto para diagnóstico
  - Risco: baixo
- 2. Adicionar preset configurável
  - Impacto: alto
  - Risco: baixo/médio, variação de qualidade/tamanho
- 3. Paralelizar cortes dos segmentos
  - Impacto: alto
  - Risco: médio, múltiplos FFmpeg simultâneos podem saturar CPU/disco
- 4. Usar stream copy quando possível
  - Impacto: muito alto
  - Risco: médio/alto, precisão de corte
- 5. Copiar áudio quando possível
  - Impacto: baixo/médio
  - Risco: baixo/médio
- 6. Evitar temporários muito grandes
  - Impacto: médio
  - Risco: baixo/médio
- 7. Melhorar planejamento antes de renderizar
  - Impacto: alto para produto
  - Risco: médio
- 8. Criar relatório do vídeo longo
  - Impacto: alto para análise
  - Risco: baixo
- 9. Cache com assinatura
  - Impacto: alto para confiabilidade
  - Risco: médio

---
# Editor IA Completo

Status: **Desenvolvimento**

Objetivo:

Transformar o projeto em um editor de vídeo autônomo.

## Capacidades Esperadas

Receber:

```txt
live_bruta.mp4 ()
```

Gerar:

```txt
Vídeos longos ()
Shorts ()
Legendas ()
Zooms ()
Efeitos ()
Títulos ()
Descrições ()
Thumbnails ()
Arquivos prontos para postagem ()
```

Sem necessidade de edição manual.

---
