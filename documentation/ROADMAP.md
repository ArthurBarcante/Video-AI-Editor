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

Status: **Concluido**
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

Projeto organizado, documentado e preparado para crescer.

---

# Fase 2 — Processamento de Vídeo

Status: Planejado

Objetivo:

Permitir leitura e manipulação de vídeos.

## Entregas

* Leitura de arquivos MP4.
* Extração de áudio.
* Validação de vídeo.
* Obtenção de metadados.
* Conversões básicas com FFmpeg.

## Resultado Esperado

O sistema consegue preparar o conteúdo para análise.

---

# Fase 3 — Transcrição

Status: Planejado

Objetivo:

Converter fala em texto.

## Entregas

* Integração com Whisper.
* Geração de transcript.json.
* Geração de SRT.
* Geração de ASS.
* Sistema de timestamps.

## Resultado Esperado

Todo conteúdo falado fica disponível para análise.

---

# Fase 4 — Sistema de Highlights

Status: Planejado

Objetivo:

Detectar automaticamente momentos interessantes.

## Entregas

* Detector de palavras-chave.
* Detector de intensidade de fala.
* Detector de exclamações.
* Detector de risadas.
* Sistema de score.
* highlights.json.

## Resultado Esperado

A IA consegue localizar candidatos a melhores momentos.

---

# Fase 5 — Planejamento de Edição

Status: Planejado

Objetivo:

Separar análise de renderização.

## Entregas

* edit_plan.json.
* Sistema de decisões.
* Planejamento de shorts.
* Planejamento de vídeos longos.
* Priorização de highlights.

## Resultado Esperado

A IA decide o que editar antes da renderização.

---

# Fase 6 — Geração de Shorts

Status: Planejado

Objetivo:

Criar vídeos curtos automaticamente.

## Entregas

* Seleção automática de trechos.
* Shorts de 15 a 45 segundos.
* Renderização automática.
* Exportação em MP4.

## Resultado Esperado

Primeira geração automática de conteúdo.

---

# Fase 7 — Geração de Vídeos Longos

Status: Planejado

Objetivo:

Montar vídeos completos utilizando os melhores momentos.

## Entregas

* Agrupamento de highlights.
* Organização narrativa.
* Criação de vídeos entre 20 e 30 minutos.
* Renderização automática.

## Resultado Esperado

Produção automática de vídeos longos para YouTube.

---

# Fase 8 — Legendas Inteligentes

Status: Planejado

Objetivo:

Melhorar a experiência visual.

## Entregas

* Estilos dinâmicos.
* Destaque de palavras.
* Quebra inteligente de linhas.
* Legendas para Shorts.
* Legendas para vídeos longos.

## Resultado Esperado

Conteúdo mais profissional e mais fácil de consumir.

---

# Fase 9 — Zooms Automáticos

Status: Planejado

Objetivo:

Destacar momentos importantes.

## Entregas

* Zoom baseado em eventos.
* Zoom baseado em palavras-chave.
* Zoom baseado em emoção.
* Configuração de intensidade.

## Resultado Esperado

Vídeos mais dinâmicos sem edição manual.

---

# Fase 10 — Efeitos Sonoros

Status: Planejado

Objetivo:

Adicionar impacto à edição.

## Entregas

* Biblioteca de SFX.
* Aplicação automática.
* Regras de uso.
* Controle de frequência.

## Resultado Esperado

Conteúdo mais envolvente.

---

# Fase 11 — Verticalização Inteligente

Status: Planejado

Objetivo:

Criar versões para Shorts e Reels.

## Entregas

* Conversão automática para 9:16.
* Crop automático.
* Blur de fundo.
* Layout adaptativo.

## Resultado Esperado

Conteúdo otimizado para dispositivos móveis.

---

# Fase 12 — IA de Contexto

Status: Futuro

Objetivo:

Entender o conteúdo além das palavras.

## Entregas

* Análise semântica.
* Entendimento de contexto.
* Agrupamento por assunto.
* Identificação de momentos importantes.

## Resultado Esperado

Highlights mais inteligentes.

---

# Fase 13 — IA de Emoção

Status: Futuro

Objetivo:

Reconhecer intensidade emocional.

## Entregas

* Detecção de surpresa.
* Detecção de raiva.
* Detecção de alegria.
* Detecção de empolgação.

## Resultado Esperado

Melhor seleção de momentos virais.

---

# Fase 14 — Títulos Automáticos

Status: Futuro

Objetivo:

Criar títulos atrativos.

## Entregas

* Geração automática de títulos.
* Múltiplas sugestões.
* Otimização para CTR.

## Resultado Esperado

Maior potencial de alcance.

---

# Fase 15 — Geração de Thumbnails

Status: Futuro

Objetivo:

Automatizar a criação de miniaturas.

## Entregas

* Captura de frames.
* Seleção de melhores imagens.
* Inserção de texto.
* Templates.

## Resultado Esperado

Pipeline completo de produção.

---

# Fase 16 — Publicação Automática

Status: Futuro

Objetivo:

Eliminar etapas manuais.

## Entregas

* Integração com YouTube.
* Integração com TikTok.
* Integração com Instagram.
* Agendamento de publicações.

## Resultado Esperado

Conteúdo publicado automaticamente.

---

# Fase 17 — Editor IA Completo

Status: Visão Final

Objetivo:

Transformar o projeto em um editor de vídeo autônomo.

## Capacidades Esperadas

Receber:

```txt
live_bruta.mp4
```

Gerar:

```txt
Vídeos longos
Shorts
Legendas
Zooms
Efeitos
Títulos
Descrições
Thumbnails
Arquivos prontos para postagem
```

Sem necessidade de edição manual.

---

# Prioridade Atual

As próximas etapas prioritárias são:

1. Estrutura do projeto.
2. Ambiente de desenvolvimento.
3. Processamento de vídeo.
4. Transcrição.
5. Sistema de highlights.
6. Planejamento de edição.

Essas etapas formarão o núcleo da primeira versão funcional.
