# 04 - Highlights

## Objetivo

Detectar automaticamente os momentos da live que têm potencial para virar shorts ou entrar no vídeo longo.

## Onde Acontece

Arquivos principais:

```text
main.py
src/highlights/detector.py
src/highlights/scorer.py
src/highlights/audio_intensity.py
src/highlights/laugh_detector.py
src/highlights/highlight_schema.py
```

## Entradas

```text
cache/transcripts/<nome>_transcript.json
cache/audio/<nome>.wav
```

## Saída

```text
cache/highlights/highlights.json
```

Formato:

```json
[
  {
    "start": 731.3,
    "end": 734.5,
    "text": "mano, não acredito nisso!",
    "score": 0.83,
    "reasons": [
      "palavra-chave: mano",
      "exclamação detectada",
      "alta intensidade de áudio"
    ]
  }
]
```

## Como Atua Hoje

1. Carrega o transcript.
2. Remove segmentos vazios.
3. Monta a lista de intervalos `start/end`.
4. Calcula energia de áudio por segmento.
5. Normaliza a energia com base no maior valor encontrado.
6. Para cada segmento:
   - detecta palavras-chave;
   - detecta exclamação;
   - detecta caixa alta;
   - avalia fala curta;
   - avalia intensidade de áudio;
   - detecta risada por texto;
   - detecta risada simples por variação de energia.
7. Soma um score.
8. Mantém apenas itens acima de `HIGHLIGHT_MIN_SCORE`.
9. Ordena por score decrescente.
10. Salva `highlights.json`.

## Palavras-Chave Atuais

```text
mano
caraca
não acredito
que isso
clipa
olha isso
meu deus
nossa
calma
pera
```

## Cache

Usa cache. Se `cache/highlights/highlights.json` já existe e `force=False`, a detecção é pulada.

## Tempo Observado

Na execução limpa:

```text
Highlights gerados: 15
Tempo aproximado: < 1s depois do transcript
```

## Gargalos

Baixo impacto no cenário atual.

A etapa já evita carregar o WAV inteiro para highlights, usando leitura por segmentos. Isso é importante para lives longas.

## Pontos De Otimização

Prioridade baixa para performance, média para qualidade.

Melhorias futuras:

- Ajustar `HIGHLIGHT_MIN_SCORE` por perfil.
- Melhorar detecção de risada.
- Adicionar blacklist de falas irrelevantes.
- Evitar highlights muito próximos entre si.
- Deduplicar trechos parecidos.
- Registrar métricas: segmentos analisados, highlights aceitos e taxa de aceitação.
