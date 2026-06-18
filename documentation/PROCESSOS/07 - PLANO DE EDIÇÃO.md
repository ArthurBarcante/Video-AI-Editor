# 07 - Plano De Edição

## Objetivo

Transformar highlights, contexto e emoções em uma decisão estruturada de edição: quais shorts serão gerados, quais segmentos entram no vídeo longo e quais ações automáticas serão aplicadas.

## Onde Acontece

Arquivos principais:

```text
main.py
src/planning/edit_planner.py
src/planning/highlight_prioritizer.py
src/planning/shorts_planner.py
src/planning/long_video_planner.py
src/planning/decision_engine.py
src/planning/edit_plan_schema.py
```

## Entradas

```text
input/<video>.mp4
cache/highlights/highlights.json
cache/context/context.json
cache/emotions/emotions.json
```

## Saída

```text
cache/edit_plans/edit_plan.json
```

## Como Atua Hoje

1. Carrega os highlights.
2. Carrega contexto, se disponível.
3. Carrega emoções, se disponível.
4. Recalcula prioridade com `prioritize_highlights()`.
5. Planeja shorts com `plan_shorts()`.
6. Planeja vídeo longo com `plan_long_videos()`.
7. Salva o `edit_plan.json`.

## Priorização

O `priority_score` parte do score original e soma bônus por:

- alta intensidade;
- risada;
- exclamação;
- palavra-chave;
- frases fortes como `"clipa"` e `"não acredito"`;
- duração adequada;
- contexto importante;
- emoção relevante.

Também penaliza:

- duração muito curta sem evento forte;
- duração acima de `60s`.

## Planejamento De Shorts

O sistema:

1. Filtra highlights com `should_be_short()`.
2. Ordena por `priority_score`.
3. Limita por `MAX_SHORTS`.
4. Expande cada short para respeitar:
   - `SHORT_MIN_DURATION`;
   - `SHORT_MAX_DURATION`.
5. Gera título automático a partir do texto.
6. Escolhe estilo.
7. Gera ações automáticas.

## Planejamento Do Vídeo Longo

O sistema:

1. Filtra highlights com `should_be_long_segment()`.
2. Ordena por `priority_score`.
3. Mantém os 80 melhores.
4. Reordena cronologicamente.
5. Expande cada segmento com contexto antes/depois.
6. Respeita duração máxima.
7. Cria `video_01`.

## Cache

Usa cache. Se `cache/edit_plans/edit_plan.json` já existe e `force=False`, a etapa é pulada.

## Tempo Observado

Na execução limpa:

```text
Shorts planejados: 5
Vídeos longos planejados: 1
Tempo aproximado: < 1s
```

## Gargalos

Baixo impacto de performance.

É uma etapa importante para qualidade, não para tempo.

## Pontos De Otimização

Prioridade baixa para performance, alta para qualidade.

Melhorias futuras:

- Evitar shorts muito parecidos.
- Evitar segmentos longos sobrepostos.
- Gerar mais de um vídeo longo por tema.
- Melhorar regras de ações automáticas.
- Criar relatório explicando por que cada corte foi escolhido.
