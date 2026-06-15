# IA Do Projeto

Este documento registra como a inteligência do Video AI Editor funciona atualmente. A IA do projeto é composta por uma parte de modelo de transcrição e por uma camada de regras heurísticas que toma decisões de edição.

## Ideia Central

O sistema não tenta editar o vídeo inteiro quadro a quadro. Ele transforma a live em dados estruturados e decide a edição em cima desses dados.

Fluxo mental da IA:

```text
fala + intensidade do áudio
        ↓
segmentos transcritos
        ↓
score de highlight
        ↓
priorização
        ↓
plano de edição
        ↓
render com ações automáticas
```

## Transcrição

A primeira camada inteligente é a transcrição com Faster Whisper.

Arquivo principal:

```text
src/transcription/whisper_transcriber.py
```

O transcritor recebe um `.wav` extraído da live e gera um JSON com:

```json
{
  "source_audio": "cache/audio/live.wav",
  "language": "pt",
  "duration": 123.4,
  "segments": [
    {
      "start": 10.0,
      "end": 13.5,
      "text": "mano, olha isso!"
    }
  ]
}
```

Configurações importantes:

`WHISPER_MODEL`
: Modelo usado pelo Faster Whisper. O padrão atual é `tiny`, priorizando velocidade.

`WHISPER_LANGUAGE`
: Idioma esperado da fala. O padrão é `pt`.

`WHISPER_DEVICE`
: Dispositivo de execução, como `cpu`.

`WHISPER_COMPUTE_TYPE`
: Tipo de computação, como `int8`, para reduzir custo em CPU.

`WHISPER_BEAM_SIZE` e `WHISPER_BEST_OF`
: Controlam busca do modelo. Valores baixos reduzem tempo.

`WHISPER_VAD_FILTER`
: Ativa filtro de voz para ignorar silêncio e ruídos.

## Limpeza De Texto

Arquivo:

```text
src/transcription/text_cleaner.py
```

Depois da transcrição, o texto é normalizado antes de entrar no restante do pipeline. Isso evita que segmentos vazios ou sujos contaminem os scores.

## Detecção De Highlights

Arquivo principal:

```text
src/highlights/detector.py
```

A detecção de highlights cruza:

1. Texto transcrito.
2. Tempo inicial e final do segmento.
3. Intensidade do áudio naquele intervalo.
4. Heurísticas de risada.
5. Palavras e sinais com potencial de corte.

O resultado é salvo em:

```text
cache/highlights/highlights.json
```

Cada highlight tem:

```json
{
  "start": 120.5,
  "end": 125.2,
  "text": "mano, olha isso!",
  "score": 0.55,
  "reasons": [
    "palavra-chave: mano",
    "palavra-chave: olha isso",
    "exclamação detectada"
  ]
}
```

## Score De Highlight

Arquivo:

```text
src/highlights/scorer.py
```

O score inicial é heurístico. Ele soma pontos quando encontra sinais fortes:

Palavras-chave:
: `mano`, `caraca`, `não acredito`, `que isso`, `clipa`, `olha isso`, `meu deus`, `nossa`, `calma`, `pera`.

Exclamação:
: Frases com `!` ganham pontos porque costumam indicar reação.

Caixa alta:
: Falas em caixa alta podem indicar grito, surpresa ou impacto.

Fala curta:
: Segmentos entre 3 e 18 palavras ganham pontos porque costumam ser bons para corte.

Intensidade de áudio:
: Energia alta ou média no áudio aumenta o score.

Risada:
: Risada textual ou provável adiciona peso ao highlight.

O score final é limitado a `1.0`.

## Intensidade De Áudio

Arquivo:

```text
src/highlights/audio_intensity.py
```

O sistema lê o WAV em PCM 16-bit e calcula RMS para cada trecho da transcrição. Depois normaliza os valores para comparar segmentos dentro da mesma live.

Essa etapa ajuda a encontrar momentos com grito, surpresa, impacto ou reação forte.

## Detecção De Risada

Arquivo:

```text
src/highlights/laugh_detector.py
```

A risada é detectada por dois caminhos:

Texto:
: Procura padrões como `kkk`, `haha` e `rsrs`.

Texto + intensidade:
: Se há indício textual de risada e o áudio está forte, o sistema aumenta a confiança.

## Score Mínimo

Configuração:

```text
HIGHLIGHT_MIN_SCORE
```

Esse valor define o corte mínimo para um segmento virar highlight. Um valor baixo, como `0.40`, deixa passar mais candidatos. Um valor alto, como `0.60`, filtra mais.

## Priorização

Arquivo:

```text
src/planning/highlight_prioritizer.py
```

Depois do score inicial, o sistema calcula `priority_score`. Esse score ajustado é usado principalmente para escolher os melhores shorts.

Sinais que aumentam prioridade:

* Alta intensidade de áudio.
* Risada.
* Exclamação.
* Palavras-chave.
* Palavras como `clipa`, `não acredito`, `meu deus`, `caraca`.
* Duração boa para corte.

Sinais que reduzem prioridade:

* Duração curta demais, exceto quando há evento forte como alta intensidade ou risada.
* Duração longa demais.

Essa camada evita que o sistema dependa apenas do score bruto.

## Motor De Decisão

Arquivo:

```text
src/planning/decision_engine.py
```

O motor de decisão responde quatro perguntas:

`should_be_short(highlight)`
: Decide se o highlight pode virar short.

`should_be_long_segment(highlight)`
: Decide se o highlight pode entrar no vídeo longo.

`choose_edit_style(highlight)`
: Define estilo: `funny`, `intense`, `highlight` ou `default`.

`generate_actions_for_highlight(highlight)`
: Cria ações automáticas de edição.

## Ações Automáticas

As ações ficam dentro do `edit_plan.json`.

Exemplo de zoom:

```json
{
  "type": "zoom",
  "intensity": 1.25,
  "target": "center",
  "reason": "zoom por alta intensidade"
}
```

Exemplo de SFX:

```json
{
  "type": "sfx",
  "time": 731.0,
  "name": "pop",
  "volume": 0.25,
  "reason": "sfx por palavra-chave"
}
```

Regras atuais:

Alta intensidade:
: Recebe zoom mais forte e SFX de impacto.

Risada:
: Recebe zoom leve e SFX de risada, se o asset existir.

Palavra-chave:
: Recebe zoom leve e SFX `pop`.

Exclamação:
: Pode receber SFX `pop` quando não caiu em regra mais forte.

## Planejamento De Shorts

Arquivo:

```text
src/planning/shorts_planner.py
```

Os shorts são escolhidos pelos melhores `priority_score`.

O planner:

1. Filtra highlights aptos para short.
2. Ordena por prioridade.
3. Limita por `MAX_SHORTS`.
4. Expande janela para respeitar `SHORT_MIN_DURATION`.
5. Corta em `SHORT_MAX_DURATION` se passar do limite.
6. Cria título automático.
7. Define estilo.
8. Adiciona ações automáticas.

## Planejamento Do Vídeo Longo

Arquivo:

```text
src/planning/long_video_planner.py
```

O vídeo longo usa highlights bons, mas mantém ordem cronológica. O sistema:

1. Filtra segmentos válidos.
2. Ordena por prioridade.
3. Limita a quantidade de candidatos.
4. Reordena por tempo.
5. Adiciona contexto antes e depois.
6. Respeita duração máxima.
7. Tenta formar um compilado útil mesmo quando não atinge a duração mínima.

## Legendas Inteligentes

Arquivos:

```text
src/subtitles/ass_generator.py
src/subtitles/line_breaker.py
src/subtitles/word_highlighter.py
```

O modo `short` usa:

* Fonte maior.
* Quebra de linha mais curta.
* Destaque de palavras importantes.

O modo `long` usa:

* Fonte mais discreta.
* Quebra de linha mais larga.

## Renderização Das Decisões

O plano não altera vídeo sozinho. Ele descreve a edição.

Quem aplica as decisões:

`src/editing/shorts_builder.py`
: Corta shorts, aplica zoom e mistura SFX quando o arquivo existe em `assets/sfx/`.

`src/editing/long_video_builder.py`
: Corta e concatena segmentos longos.

`src/rendering/verticalizer.py`
: Cria versão 9:16 com fundo blur e vídeo centralizado.

## Limites Da IA Atual

A IA atual é explicável e baseada em heurísticas. Ela ainda não entende contexto profundo da live, piadas longas ou narrativa completa.

Pontos fortes:

* Rápida.
* Auditável.
* Barata de executar.
* Fácil de ajustar por regras.

Pontos fracos:

* Pode perder momentos bons sem palavra-chave ou energia alta.
* Pode escolher falso positivo quando uma palavra-chave aparece em contexto fraco.
* Não entende ainda arco narrativo completo.

## Como Melhorar No Futuro

Possíveis evoluções:

* Usar modelo de linguagem para resumir contexto.
* Detectar mudança de assunto.
* Agrupar highlights por tema.
* Detectar emoção pela voz.
* Usar visão computacional para gameplay, rosto ou chat.
* Aprender com cortes aprovados ou rejeitados pelo usuário.
