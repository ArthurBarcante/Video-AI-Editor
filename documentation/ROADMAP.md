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

Status: **Desenvolvimento**

Objetivo:

Entender o conteúdo além das palavras.

## Entregas

* Análise semântica. ()
* Entendimento de contexto. ()
* Agrupamento por assunto. ()
* Identificação de momentos importantes. ()

## Resultado Esperado

Highlights mais inteligentes.

---

# Fase 13 — IA de Emoção

Status: **Desenvolvimento**

Objetivo:

Reconhecer intensidade emocional.

## Entregas

* Detecção de surpresa. ()
* Detecção de raiva. ()
* Detecção de alegria. ()
* Detecção de empolgação. ()

## Resultado Esperado

Melhor seleção de momentos virais.

---

# Fase 14 — Títulos Automáticos

Status: **Futuro**

Objetivo:

Criar títulos atrativos.

## Entregas

* Geração automática de títulos. ()
* Múltiplas sugestões. ()
* Otimização para CTR. ()

## Resultado Esperado

Maior potencial de alcance.

---

# Fase 15 — Geração de Thumbnails

Status: **Futuro**

Objetivo:

Automatizar a criação de miniaturas.

## Entregas

* Captura de frames. ()
* Seleção de melhores imagens. ()
* Inserção de texto. ()
* Templates. ()

## Resultado Esperado

Pipeline completo de produção.

---

# Fase 16 — Publicação Automática

Status: **Futuro**

Objetivo:

Eliminar etapas manuais.

## Entregas

* Integração com YouTube. ()
* Integração com TikTok. ()
* Integração com Instagram. ()
* Agendamento de publicações. ()

## Resultado Esperado

Conteúdo publicado automaticamente.

---

# Fase 17 — Editor IA Completo

Status: **Visão Final**

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

# Fase 18 - Otimizar Edição para Funcionar com Brutos de Live

Status: **Futuro**

Objetivo:

Melhorar tempo de edição e agilizar etapas

## Entregas

* Código limpo e otimizado. ()
* Execução das tarefas em 40-60 min de uma live de 5-6 horas. ()
* Shorts de 15 - 45 segundos completamente editados corretamente. ()
* Vídeos de 20-30 min editados corretamente. ()

## Resultado Esperado

Rapidez e agilidade do script

---

---

# Fase 19 — Legendas Geradas por Cortes

Status: **Futuro**

Objetivo:

Melhorar edição de Shorts e otimizá-la

## Entregas

* Criação de .ass por shorts ()
* Legendas separadas por corte ()

## Resultado Esperado

Legendas diferentes entre si para facilitar edição de shorts

---
# Fase 20 - Zoom Temporal

Status: **Futuro**

Objetivo:

Melhorar efeito de Zoom

## Entregas

* FFMpeg usando enable='between(t,start,end)' ()
* Efeitos de zoom preciso ()

## Resultado Esperado

Zooms precisos e com intervalos de tempos claros

---

# Fase 21 - Shorts Melhores

Status: **Futuro**

Objetivo:

Melhorar visual dos shorts

## Entregas

* Modo blur_background. ()
* Modo center_crop. ()
* Modo top_gameplay_bottom_facecam. ()
* Modo facecam_priority ()

## Resultado Esperado

Shorts variados com visuais diferentes dependendo do modo

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
