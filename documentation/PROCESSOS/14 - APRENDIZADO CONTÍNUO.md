# 14 - Aprendizado Contínuo

## Objetivo

Registrar feedback e correções para que o projeto reaproveite preferências do canal em execuções futuras.

## Onde Acontece

Arquivos principais:

```text
src/learning/feedback_schema.py
src/learning/feedback_collector.py
src/learning/correction_memory.py
src/learning/learning_rules.py
src/learning/learning_applier.py
src/transcription/text_cleaner.py
```

## Entradas

```text
correções manuais
feedback de highlights
feedback de edição
preferências do canal
```

## Saídas

```text
cache/learning/feedback.json
cache/learning/corrections.json
cache/learning/successful_patterns.json
cache/learning/learning_profile.json
```

## Como Atua Hoje

A primeira implementação atua na transcrição.

O usuário pode registrar uma correção:

```json
{
  "type": "transcription_error",
  "wrong": "forte naite",
  "correct": "Fortnite",
  "context": "nome de jogo",
  "apply_future": true
}
```

Quando `apply_future=true`, a correção também entra em:

```text
cache/learning/corrections.json
```

Exemplo:

```json
{
  "transcription_replacements": {
    "forte naite": "Fortnite",
    "chat gbt": "ChatGPT"
  }
}
```

Na próxima transcrição, `src/transcription/text_cleaner.py` aplica essas substituições automaticamente.

## Perfil De Aprendizado

O arquivo `cache/learning/learning_profile.json` guarda preferências globais:

```json
{
  "transcription": {
    "preferred_replacements": {}
  },
  "highlights": {
    "keyword_weight": 0.15,
    "laugh_weight": 0.25,
    "emotion_weight": 0.3,
    "audio_intensity_weight": 0.2
  },
  "editing": {
    "default_zoom_intensity": 1.12,
    "max_sfx_per_short": 1,
    "short_padding_before": 2.0,
    "short_padding_after": 1.5
  },
  "subtitles": {
    "max_words_per_line": 4,
    "max_lines": 2,
    "style": "bold_clean"
  }
}
```

## Limite Atual

Ainda não há treinamento de modelo.

O aprendizado atual é por:

- regras;
- feedback salvo localmente;
- memória de correções;
- perfil de preferências.

## Próximos Passos

- Aplicar pesos do `learning_profile.json` na priorização de highlights.
- Registrar feedback de shorts bons/ruins.
- Ajustar zoom, SFX e padding com base em feedback de edição.
- Aplicar preferências de legenda no segmentador de shorts.
