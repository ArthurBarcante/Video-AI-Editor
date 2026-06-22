# 15 - Analytics

## Objetivo

Comparar os vídeos gerados com métricas reais de publicação para descobrir padrões que funcionaram e alimentar o aprendizado contínuo.

## Onde Acontece

Arquivos principais:

```text
src/analytics/video_metrics_schema.py
src/analytics/metrics_collector.py
src/analytics/performance_analyzer.py
src/analytics/learning_from_metrics.py
src/learning/correction_memory.py
```

## Entrada Manual Inicial

Antes de integrar APIs externas, o sistema usa:

```text
data/analytics/manual_video_metrics.csv
```

Colunas esperadas:

```text
video_id,platform,views,likes,comments,shares,average_view_duration,retention_rate,ctr
```

Exemplo:

```csv
short_01,youtube_shorts,12000,930,45,80,23.8,0.73,0.09
```

## Saídas

```text
cache/analytics/video_metrics.json
cache/analytics/performance_report.json
cache/analytics/learned_patterns.json
cache/learning/learning_profile.json
```

## Como Atua Hoje

O fluxo atual é manual e seguro:

1. O usuário preenche `manual_video_metrics.csv`.
2. `metrics_collector.py` cruza as métricas com `cache/edit_plans/edit_plan.json`.
3. O sistema enriquece cada vídeo com features do short:
   - score do highlight;
   - estilo;
   - zoom;
   - SFX;
   - duração;
   - título.
4. `performance_analyzer.py` calcula padrões dos melhores vídeos.
5. `learning_from_metrics.py` aplica os padrões em `learning_profile.json`.

## Padrões Aprendidos

O sistema começa a inferir:

- melhor faixa de duração;
- emoções com maior retenção;
- padrões de título com melhor CTR;
- limite de SFX antes de penalizar retenção;
- intensidade média de zoom nos melhores shorts.

Exemplo:

```json
{
  "analytics_learning": {
    "best_short_duration_range": [25, 35],
    "best_emotions": ["surprise", "hype"],
    "preferred_title_patterns": ["NÃO ACREDITO", "AO VIVO"],
    "sfx_penalty_if_more_than": 1,
    "zoom_preferred_intensity": 1.12
  }
}
```

## Limite Atual

Ainda não há coleta automática de YouTube, TikTok ou Instagram.

O objetivo desta etapa é aprender sem depender de OAuth, permissões e revisão de app.

## Próximos Passos

- Criar comando para importar CSV e aplicar aprendizado.
- Cruzar padrões aprendidos com `highlight_prioritizer.py`.
- Usar duração ideal no planejamento de shorts.
- Usar padrões de título no `title_generator.py`.
- Integrar APIs oficiais de analytics quando a camada manual estiver validada.
