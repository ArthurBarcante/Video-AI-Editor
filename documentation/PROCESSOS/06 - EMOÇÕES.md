# 06 - Emoções

## Objetivo

Detectar intensidade emocional nas falas para favorecer momentos com mais potencial de retenção e viralização.

## Onde Acontece

Arquivos principais:

```text
main.py
src/emotion/emotion_analyzer.py
src/emotion/emotion_rules.py
src/emotion/emotion_schema.py
src/highlights/audio_intensity.py
```

## Entradas

```text
cache/transcripts/<nome>_transcript.json
cache/audio/<nome>.wav
```

## Saída

```text
cache/emotions/emotions.json
```

Formato:

```json
{
  "source_transcript": "cache/transcripts/live_transcript.json",
  "source_audio": "cache/audio/live.wav",
  "segments": [
    {
      "start": 120.5,
      "end": 123.8,
      "text": "mano, não acredito nisso!",
      "emotion": "surprise",
      "emotion_score": 0.53,
      "audio_intensity": 0.72,
      "reasons": [
        "surpresa: não acredito",
        "exclamação detectada",
        "alta intensidade de áudio"
      ]
    }
  ]
}
```

## Como Atua Hoje

1. Carrega o transcript.
2. Remove segmentos vazios.
3. Carrega o WAV inteiro em memória.
4. Calcula energia de áudio para cada segmento.
5. Normaliza a energia.
6. Detecta emoção por palavras.
7. Soma bônus de intensidade se a emoção não for neutra.
8. Salva a análise emocional por segmento.

## Emoções Atuais

```text
surprise
anger
joy
hype
neutral
```

## Regras Atuais

Exemplos:

- `"não acredito"`, `"que isso"`, `"caraca"` aumentam surpresa.
- `"droga"`, `"merda"`, `"que raiva"` aumentam raiva.
- `"boa"`, `"ganhei"`, `"kkkk"` aumentam alegria.
- `"vamos"`, `"clipa"`, `"absurdo"` aumentam empolgação.
- `"!"` aumenta hype e surpresa.

## Cache

Usa cache. Se `cache/emotions/emotions.json` já existe e `force=False`, a etapa é pulada.

## Tempo Observado

Na execução limpa:

```text
Segmentos analisados: 1302
Tempo aproximado: < 1s
```

## Gargalos

Hoje foi rápido, mas existe um risco para lives muito longas: esta etapa carrega o WAV inteiro em memória.

Para `57min`, isso foi aceitável. Para `5-6h`, pode consumir memória e I/O de forma mais perceptível.

## Pontos De Otimização

Prioridade média para lives longas.

Melhorias futuras:

- Reaproveitar cálculo de energia dos highlights.
- Calcular energia por streaming, sem carregar o WAV inteiro.
- Salvar métricas de distribuição emocional.
- Cruzar emoção com contexto para priorização.
- Melhorar regras por tipo de conteúdo.
