# Lógicas Do Sistema

Este documento explica como o projeto funciona no macro. A leitura ideal é seguir a ordem do pipeline, porque o sistema é uma sequência de transformação de dados: vídeo bruto entra, arquivos intermediários são criados, um plano de edição é montado e os vídeos finais são renderizados.

## Visão Geral

Fluxo principal:

```text
input/live.mp4
    ↓
validação e metadados
    ↓
cache/audio/live.wav
    ↓
cache/transcripts/live_transcript.json
    ↓
output/subtitles/
    ↓
cache/highlights/highlights.json
    ↓
cache/context/context.json
    ↓
cache/emotions/emotions.json
    ↓
cache/edit_plans/edit_plan.json
    ↓
output/shorts/
    ↓
output/vertical/
    ↓
output/long/
```

O orquestrador desse fluxo é:

```text
main.py
```

## 1. Preparação Das Pastas

Logo no início, o sistema chama:

```python
ensure_project_dirs()
```

Essa função cria as pastas necessárias:

```text
input/
cache/
output/
assets/
```

Isso reduz erro de execução quando o projeto está rodando pela primeira vez em outra máquina.

## 2. Localização Do Vídeo

O sistema procura o primeiro `.mp4` em:

```text
input/
```

Arquivo responsável:

```text
src/video/reader.py
```

Regra atual:

* Só aceita `.mp4`.
* Se não houver vídeo, lança erro.
* Se houver vários vídeos, usa o primeiro em ordem alfabética.

## 3. Validação Do Vídeo

Arquivo responsável:

```text
src/video/validator.py
```

A validação confirma:

* O arquivo existe.
* É um arquivo, não uma pasta.
* Tem extensão `.mp4`.
* Não está vazio.
* Possui stream de vídeo.
* Possui stream de áudio.

Essa etapa evita iniciar transcrição ou render em cima de arquivo inválido.

## 4. Metadados

Arquivo responsável:

```text
src/video/metadata.py
```

O sistema usa FFprobe para ler:

* Duração.
* Tamanho.
* Bitrate.
* Codec de vídeo.
* Codec de áudio.
* Largura.
* Altura.
* FPS.

Esses dados são úteis para logs, validação e futuras decisões de edição.

## 5. Extração De Áudio

Arquivo responsável:

```text
src/audio/extractor.py
```

Entrada:

```text
input/live.mp4
```

Saída:

```text
cache/audio/live.wav
```

O FFmpeg extrai áudio em:

* WAV.
* Mono.
* PCM 16-bit.
* 16 kHz.

Esse formato é usado porque é leve para transcrição e análise de intensidade.

Se o áudio já existe e `force=False`, o sistema usa cache.

## 6. Transcrição

Arquivo responsável:

```text
src/transcription/whisper_transcriber.py
```

Entrada:

```text
cache/audio/live.wav
```

Saída:

```text
cache/transcripts/live_transcript.json
```

O Faster Whisper transforma áudio em segmentos:

```json
{
  "start": 10.0,
  "end": 14.5,
  "text": "mano, não acredito nisso!"
}
```

Cada segmento vira base para:

* Legendas.
* Highlights.
* Contexto.
* Emoções.
* Planejamento de cortes.

## 7. Geração De Legendas

Arquivos responsáveis:

```text
src/subtitles/srt_generator.py
src/subtitles/ass_generator.py
```

Saídas:

```text
output/subtitles/live_transcript.srt
output/subtitles/live_transcript_short.ass
output/subtitles/live_transcript_long.ass
```

O `.srt` é simples e portável.

O `.ass` permite estilo visual:

* Modo `short`: legenda maior, mais impactante, com destaque de palavras.
* Modo `long`: legenda mais limpa e discreta.

## 8. Detecção De Highlights

Arquivo responsável:

```text
src/highlights/detector.py
```

Entradas:

```text
cache/transcripts/live_transcript.json
cache/audio/live.wav
```

Saída:

```text
cache/highlights/highlights.json
```

O detector percorre cada segmento transcrito e calcula sinais:

* Palavra-chave.
* Exclamação.
* Caixa alta.
* Duração da fala.
* Intensidade do áudio.
* Risada.

Se o score passa de `HIGHLIGHT_MIN_SCORE`, o segmento vira highlight.

## 9. Análise De Contexto

Arquivo responsável:

```text
src/context/context_analyser.py
```

Entrada:

```text
cache/transcripts/live_transcript.json
```

Saída:

```text
cache/context/context.json
```

O sistema agrupa segmentos próximos da transcrição em blocos maiores. Depois extrai palavras relevantes, infere um tópico e calcula `importance_score`.

Essa etapa permite que um highlight seja avaliado pelo que estava acontecendo ao redor, e não só pela frase isolada.

## 10. Análise De Emoção

Arquivo responsável:

```text
src/emotion/emotion_analyzer.py
```

Entradas:

```text
cache/transcripts/live_transcript.json
cache/audio/live.wav
```

Saída:

```text
cache/emotions/emotions.json
```

O sistema detecta emoções por texto e intensidade de áudio:

* Surpresa.
* Raiva.
* Alegria.
* Empolgação.
* Neutralidade.

Essa etapa cria uma base para escolher momentos com mais potencial viral.

## 11. Priorização Dos Highlights

Arquivo responsável:

```text
src/planning/highlight_prioritizer.py
```

Nem todo highlight bom é igualmente bom para short.

Por isso o sistema calcula `priority_score`, que ajusta o score original com sinais extras:

* Alta intensidade.
* Risada.
* Exclamação.
* Palavra-chave.
* Duração boa.
* Importância do contexto.
* Emoção detectada.

Esse score ajuda a escolher os cortes mais fortes primeiro.

## 12. Plano De Edição

Arquivo responsável:

```text
src/planning/edit_planner.py
```

Entrada:

```text
cache/highlights/highlights.json
cache/context/context.json
cache/emotions/emotions.json
```

Saída:

```text
cache/edit_plans/edit_plan.json
```

O plano de edição é o contrato central do sistema. Ele diz o que será renderizado.

Estrutura macro:

```json
{
  "source_video": "input/live.mp4",
  "shorts": [],
  "long_videos": []
}
```

## 13. Planejamento De Shorts

Arquivo responsável:

```text
src/planning/shorts_planner.py
```

O planner de shorts:

1. Filtra highlights aptos.
2. Ordena por prioridade.
3. Limita por `MAX_SHORTS`.
4. Expande duração mínima.
5. Limita duração máxima.
6. Gera título automático.
7. Escolhe estilo.
8. Gera ações.

Exemplo:

```json
{
  "id": "short_01",
  "start": 670.64,
  "end": 685.64,
  "duration": 15.0,
  "score": 0.8,
  "title": "POOOOO!",
  "style": "intense",
  "actions": [
    {
      "type": "zoom",
      "intensity": 1.25,
      "target": "center",
      "reason": "zoom por alta intensidade"
    }
  ]
}
```

## 14. Planejamento Do Vídeo Longo

Arquivo responsável:

```text
src/planning/long_video_planner.py
```

O vídeo longo usa highlights bons, mas precisa preservar ordem cronológica.

Fluxo:

1. Filtra highlights válidos.
2. Seleciona os melhores por prioridade.
3. Limita excesso.
4. Ordena por `start`.
5. Adiciona contexto antes e depois.
6. Garante que a soma não passe da duração máxima.

Saída:

```json
{
  "id": "video_01",
  "title": "Melhores momentos da live",
  "segments": []
}
```

## 15. Motor De Decisão

Arquivo responsável:

```text
src/planning/decision_engine.py
```

Esse arquivo concentra as regras que transformam highlights em decisões de edição.

Ele define:

* Se vira short.
* Se entra no vídeo longo.
* Qual estilo visual recebe.
* Quais ações automáticas entram no plano.

Ações atuais:

`zoom`
: Usado para destacar momentos intensos, risadas e palavras-chave.

`sfx`
: Usado para adicionar sons curtos como `pop`, `impact` ou `laugh`.

## 16. Renderização Dos Shorts

Arquivo responsável:

```text
src/editing/shorts_builder.py
```

Entrada:

```text
cache/edit_plans/edit_plan.json
```

Saída:

```text
output/shorts/short_01.mp4
```

O builder:

1. Corta o trecho do vídeo original.
2. Aplica zoom se existir action `zoom`.
3. Resolve SFX em `assets/sfx/`.
4. Mistura SFX no áudio se o asset existir.
5. Exporta em H.264/AAC.

## 17. Verticalização

Arquivo responsável:

```text
src/rendering/verticalizer.py
```

Entrada:

```text
output/shorts/short_01.mp4
```

Saída:

```text
output/vertical/short_01_vertical.mp4
```

O layout final é 9:16:

```text
fundo blur
vídeo real centralizado
fundo blur
```

Essa estratégia evita cortar informação importante do gameplay.

## 18. Renderização Do Vídeo Longo

Arquivo responsável:

```text
src/editing/long_video_builder.py
```

Entrada:

```text
cache/edit_plans/edit_plan.json
```

Saída:

```text
output/long/video_01.mp4
```

O builder:

1. Corta cada segmento planejado.
2. Salva segmentos temporários.
3. Cria um arquivo de concatenação.
4. Junta tudo com FFmpeg.
5. Remove temporários.

## 19. Cache

O projeto usa cache para evitar retrabalho.

Se um arquivo já existe e `force=False`, a etapa geralmente reaproveita o resultado.

Exemplos:

* Áudio já extraído.
* Transcrição já feita.
* Highlights já detectados.
* Contexto já analisado.
* Emoções já analisadas.
* Plano já gerado.
* Shorts já renderizados.
* Verticais já renderizados.
* Vídeo longo já renderizado.

Para forçar nova execução, apague o arquivo desejado ou use funções com `force=True` em testes/código.

## 20. Resultado Final

Depois do pipeline, os principais arquivos são:

```text
cache/highlights/highlights.json
cache/context/context.json
cache/emotions/emotions.json
cache/edit_plans/edit_plan.json
output/subtitles/
output/shorts/
output/vertical/
output/long/
```

O `edit_plan.json` é o melhor ponto para auditar se a lógica tomou boas decisões antes de olhar os vídeos finais.

## 21. Onde Ajustar Comportamento

Mais ou menos highlights:
: Ajustar `HIGHLIGHT_MIN_SCORE` no `.env`.

Mais ou menos shorts:
: Ajustar `MAX_SHORTS`.

Duração dos shorts:
: Ajustar `SHORT_MIN_DURATION` e `SHORT_MAX_DURATION`.

Modelo de transcrição:
: Ajustar `WHISPER_MODEL`.

Regras de highlight:
: Editar `src/highlights/scorer.py`.

Priorização:
: Editar `src/planning/highlight_prioritizer.py`.

Contexto:
: Editar `src/context/semantic_analyzer.py` e `src/context/topic_grouper.py`.

Emoção:
: Editar `src/emotion/emotion_rules.py` e `src/emotion/emotion_analyzer.py`.

Ações automáticas:
: Editar `src/planning/decision_engine.py`.

Render dos shorts:
: Editar `src/editing/shorts_builder.py`.

Verticalização:
: Editar `src/rendering/verticalizer.py`.
