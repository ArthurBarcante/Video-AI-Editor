# Validação Geral - 2026-06-22

## Objetivo

Validar o estado atual do projeto, registrar erros encontrados no processo, gargalos observados e a evolução da IA do editor.

## Comandos Executados

```bash
./.venv/bin/python -m ruff check .
./.venv/bin/python -m pytest
./.venv/bin/python main.py --video "input/Vi o ICEBERG da CALVOESFERA e meu DEUS me ajude - Core 2 (720p, h264, youtube).mp4"
```

## Resultado Dos Testes

```text
Ruff: All checks passed
Pytest: 110 passed
Pipeline principal: executado com sucesso
```

## Artefatos Validados

```text
output/shorts/: 5 vídeos
output/vertical/: 5 vídeos verticais
output/long/: 1 vídeo + 1 relatório JSON
output/thumbnails/: 6 thumbnails finais
output/subtitles/: SRT, ASS global e ASS individual por short
cache/analytics/: métricas, relatório e padrões aprendidos
cache/learning/: feedback, correções, padrões e perfil de aprendizado
```

## Tempos Observados No Teste De Integração

Arquivo testado:

```text
input/Vi o ICEBERG da CALVOESFERA e meu DEUS me ajude - Core 2 (720p, h264, youtube).mp4
```

Metadados principais:

```text
Duração do vídeo/áudio: 3441.20s
Extração de áudio: 35.23s
Transcrição: 183.27s
Velocidade realtime da transcrição: 18.78x
Chunks de transcrição: 4
Chunks reutilizados do cache: 0
Segmentos gerados: 1178
Render dos shorts com cache: 0.01s
Verticalização com cache: 0.01s
```

Após correção dos problemas encontrados, foi executada nova validação:

```text
Pytest: 110 passed
Primeira execução pós-correção:
- Render dos shorts: 25.90s
- Verticalização: 119.59s
- Vídeo longo: 63.79s

Segunda execução com metadados de cache:
- Render dos shorts: 0.03s
- Verticalização: 0.03s
- Pipeline principal concluído com cache validado

Validação final antes de avançar para otimização:
- Ruff: `All checks passed`
- Pytest: `110 passed`
- Pipeline principal executado em sequência, sem erro
- Render dos shorts: `26.47s`
- Verticalização: `118.80s`
- Vídeo longo: `61.48s`
```

## Erros Corrigidos

1. Analytics aprendia com métrica zerada.
   - Sintoma: o CSV manual de exemplo tinha views/retenção/CTR zerados, mas o sistema gerava padrões aprendidos mesmo assim.
   - Impacto: `learning_profile.json` poderia ser contaminado por dados falsos.
   - Ação tomada: corrigido. O analisador agora ignora linhas sem métricas reais.
   - Status: corrigido e validado por teste automatizado.

2. Mudança de assinatura do áudio invalidou o cache antigo de transcrição.
   - Sintoma: o `main.py` reextraiu áudio para `cache/audio/<nome>_7c655c5a01fe.wav` e gerou uma nova transcrição, mesmo já existindo uma transcrição antiga sem hash.
   - Impacto: execução de integração levou vários minutos em vez de reaproveitar tudo.
   - Status: mitigado. Depois da primeira execução com assinatura nova, áudio e transcrição passaram a ser reutilizados corretamente.

3. Caches downstream foram reutilizados após nova transcrição.
   - Sintoma: highlights, contexto, emoções e edit plan foram reaproveitados do cache antigo mesmo depois da nova transcrição com hash.
   - Impacto: risco de inconsistência se o transcript novo divergir do transcript antigo.
   - Ação tomada: corrigido. Artefatos agora salvam `.meta.json` com assinatura das entradas usadas.
   - Etapas cobertas: highlights, contexto, emoções, edit plan, legendas individuais, títulos, thumbnails, shorts, verticalização, vídeo longo e plano de publicação.
   - Status: corrigido e validado no `main.py`.

4. Vídeo longo atual estava curto.
   - Sintoma anterior: `segment_count=1`, `planned_duration=11.0s`.
   - Impacto: era um falso vídeo longo.
   - Ação tomada: corrigido. O planejador não cria vídeo longo quando há menos de `60s` de material.
   - Resultado no vídeo real: `segment_count=8`, `planned_duration=153.74s`.
   - Status: corrigido.

## Erros Abertos

```text
Nenhum erro aberto após a rodada de correção e validação.
```

## Gargalos Observados

1. Transcrição continua sendo o maior custo do pipeline.
   - Tempo observado: `183.27s`.
   - Mesmo otimizada, ainda domina o tempo total quando o cache não é reaproveitado.
   - Próxima melhoria recomendada: cache parcial mais estável por assinatura e reaproveitamento entre mudanças de nome/hash.

2. Extração de áudio ainda custa tempo perceptível.
   - Tempo observado: `35.23s`.
   - O WAV gerado tem cerca de `105 MB`.
   - Próxima melhoria recomendada: evitar reextração quando a assinatura do vídeo já foi processada.

3. Cache ainda não é dependente da árvore completa do pipeline.
   - Exemplo: transcript novo, mas highlights/contexto/emoções antigos.
   - Status: corrigido nesta rodada com arquivos `.meta.json`.

4. Verticalização continua sendo gargalo quando precisa renderizar do zero.
   - Tempo observado após invalidar cache antigo: `119.59s`.
   - Segunda execução com cache validado: `0.03s`.
   - Próxima melhoria recomendada: verticalização direta do original ou reaproveitamento estrutural mais agressivo.

5. Analytics precisa de amostra mínima.
   - Com poucos vídeos, padrões podem ser instáveis.
   - Estado atual: sem erro aberto. O CSV de exemplo tem métricas zeradas e agora é ignorado pelo aprendizado.
   - Próxima melhoria recomendada: só aplicar aprendizado de analytics com amostra mínima, por exemplo `5` a `10` shorts publicados.

## Evolução Da IA Do Projeto

1. IA deixou de depender apenas de heurísticas fixas.
   - Agora existe `cache/learning/learning_profile.json`.
   - O projeto tem memória local para preferências e correções.

2. Transcrição ganhou aprendizado por correções.
   - Correções em `cache/learning/corrections.json` passam a ser aplicadas pelo `text_cleaner.py`.
   - Exemplo esperado: `forte naite` vira `Fortnite`.

3. Analytics real começou a alimentar aprendizado.
   - Nova camada `src/analytics/`.
   - Métricas manuais podem ser importadas por CSV.
   - O sistema cruza métricas com `edit_plan.json` e descobre padrões.

4. Legendas ficaram mais inteligentes para shorts.
   - Agora há `.ass` individual por short.
   - Timestamps são relativos ao corte.
   - Segmentos longos são divididos por palavras e duração.

5. Planejamento já usa sinais semânticos e emocionais.
   - O projeto possui contexto, emoções, priorização de highlights e plano de edição com ações.
   - A próxima evolução é fazer `learning_profile.json` influenciar esses pesos diretamente.

## Próximas Ações Recomendadas

1. Criar comando para analytics.
   - Exemplo: `./.venv/bin/python -m scripts.import_analytics`.
   - Motivo: importar CSV, gerar relatório e atualizar aprendizado em uma única ação.

2. Exigir amostra mínima antes de aplicar analytics ao perfil.
   - Prioridade: alta.
   - Motivo: impedir aprendizado precipitado.

3. Usar `analytics_learning` no planejamento.
   - Aplicar duração ideal em `shorts_planner.py`.
   - Aplicar padrões de título em `title_generator.py`.
   - Ajustar zoom/SFX em `decision_engine.py`.

## Conclusão

O projeto está funcional e validado pelos testes automatizados. Os principais problemas encontrados na validação foram corrigidos: analytics não aprende mais com dados zerados, caches agora são invalidados por assinatura das entradas e o vídeo longo não é mais criado quando há material insuficiente. A IA evoluiu para uma arquitetura com memória e aprendizado por métricas, mas ainda precisa de dados reais e regras de aplicação mais conservadoras para evitar aprendizado prematuro.
