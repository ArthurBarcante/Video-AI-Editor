# 05 - Contexto

## Objetivo

Entender o que estava acontecendo ao redor das falas destacadas, para que o sistema não dependa apenas de frases isoladas.

## Onde Acontece

Arquivos principais:

```text
main.py
src/context/context_analyser.py
src/context/topic_grouper.py
src/context/semantic_analyzer.py
src/context/context_schema.py
```

## Entrada

```text
cache/transcripts/<nome>_transcript.json
```

## Saída

```text
cache/context/context.json
```

Formato:

```json
{
  "source_transcript": "cache/transcripts/live_transcript.json",
  "blocks": [
    {
      "id": "context_001",
      "start": 120.5,
      "end": 184.2,
      "duration": 63.7,
      "text": "agora eu vou tentar passar desse boss...",
      "keywords": ["boss", "morri"],
      "topic": "progressão de gameplay",
      "importance_score": 0.62,
      "reasons": [
        "termos relevantes detectados",
        "tópico relevante: progressão de gameplay"
      ]
    }
  ]
}
```

## Como Atua Hoje

1. Carrega o transcript.
2. Agrupa segmentos em blocos maiores.
3. Um bloco continua enquanto:
   - o intervalo entre falas é menor ou igual a `8s`;
   - a duração total do bloco não passa de `90s`.
4. Junta os textos do bloco.
5. Extrai palavras relevantes.
6. Infere um tópico.
7. Calcula `importance_score`.
8. Salva os blocos em `context.json`.

## Tópicos Atuais

O sistema identifica tópicos simples como:

```text
progressão de gameplay
falha ou derrota
vitória ou conquista
momentos inesperados
estratégia
assunto relevante
conversa geral
```

## Cache

Usa cache. Se `cache/context/context.json` já existe e `force=False`, a etapa é pulada.

## Tempo Observado

Na execução limpa:

```text
Blocos gerados: 40
Tempo aproximado: < 1s
```

## Gargalos

Baixo impacto. É uma etapa textual e barata.

## Pontos De Otimização

Prioridade baixa para performance, média para qualidade.

Melhorias futuras:

- Criar tópicos mais específicos por jogo ou categoria.
- Ajustar `max_gap` e `max_duration`.
- Usar contexto para descartar highlights ruins.
- Usar contexto para gerar títulos e descrições melhores.
- Registrar distribuição de tópicos e scores.
