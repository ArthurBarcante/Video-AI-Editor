# Estrutura do Projeto

Este documento explica a organização de pastas, arquivos, extensões, bibliotecas e dependências do projeto **Video AI Editor**.

O objetivo é manter o projeto organizado, modular e fácil de evoluir.

---

# Visão Geral da Estrutura

```txt
video-ai-editor/
├── main.py
├── README.md
├── ESTRUTURA.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── input/
│   └── .gitkeep
│
├── output/
│   ├── long/
│   │   └── .gitkeep
│   ├── shorts/
│   │   └── .gitkeep
│   ├── vertical/
│   │   └── .gitkeep
│   └── subtitles/
│       └── .gitkeep
│
├── cache/
│   ├── audio/
│   │   └── .gitkeep
│   ├── transcripts/
│   │   └── .gitkeep
│   ├── highlights/
│   │   └── .gitkeep
│   └── edit_plans/
│       └── .gitkeep
│
├── assets/
│   ├── sfx/
│   │   └── .gitkeep
│   ├── fonts/
│   │   └── .gitkeep
│   └── overlays/
│       └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── paths.py
│   │   └── settings.py
│   ├── audio/
│   │   ├── __init__.py
│   │   └── extractor.py
│   ├── transcription/
│   │   ├── __init__.py
│   │   └── whisper_transcriber.py
│   ├── subtitles/
│   │   ├── __init__.py
│   │   ├── srt_generator.py
│   │   ├── ass_generator.py
│   │   └── subtitle_renderer.py
│   ├── highlights/
│   │   ├── __init__.py
│   │   ├── detector.py
│   │   └── scorer.py
│   ├── planning/
│   │   ├── __init__.py
│   │   └── edit_planner.py
│   ├── editing/
│   │   ├── __init__.py
│   │   ├── long_video_builder.py
│   │   └── shorts_builder.py
│   ├── rendering/
│   │   ├── __init__.py
│   │   ├── ffmpeg_utils.py
│   │   ├── video_renderer.py
│   │   └── verticalizer.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       ├── file_utils.py
│       └── time_utils.py
│
├── tests/
│   └── .gitkeep
│
└── .vscode/
    ├── settings.json
    ├── launch.json
    └── extensions.json
```

---

# Arquivos da Raiz

## `main.py`

Arquivo principal do projeto.

Ele deve funcionar como orquestrador do pipeline.

Responsabilidades:

* iniciar o fluxo principal;
* carregar configurações;
* localizar o vídeo de entrada;
* chamar os módulos na ordem correta;
* controlar o fluxo geral da aplicação.

O `main.py` não deve conter regras complexas de edição, transcrição ou renderização.

Exemplo de responsabilidade correta:

```python
def main():
    extract_audio()
    transcribe_audio()
    detect_highlights()
    generate_edit_plan()
    render_outputs()
```

---

## `README.md`

Documento principal do projeto.

Serve para explicar:

* o que é o projeto;
* qual problema ele resolve;
* qual é a proposta;
* quais são os objetivos;
* qual é o status atual;
* qual é o roadmap.

O README deve ser escrito para qualquer pessoa que visite o repositório pela primeira vez.

---

## `ESTRUTURA.md`

Documento técnico da estrutura do projeto.

Serve para explicar:

* organização das pastas;
* função de cada arquivo;
* dependências;
* bibliotecas;
* extensões recomendadas;
* padrões usados no projeto.

---

## `requirements.txt`

Lista de dependências Python do projeto.

Exemplo inicial:

```txt
faster-whisper
moviepy
ffmpeg-python
python-dotenv
pydantic
rich
ruff
pytest
```

Esse arquivo permite instalar as dependências com:

```bash
pip install -r requirements.txt
```

---

## `.gitignore`

Arquivo que define o que não deve ser versionado pelo Git.

Deve ignorar:

* ambiente virtual;
* arquivos temporários;
* cache;
* vídeos brutos;
* vídeos renderizados;
* arquivos `.env`;
* arquivos Python compilados.

Exemplo:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc

input/*.mp4
input/*.mov
input/*.mkv

output/*
!output/**/.gitkeep

cache/*
!cache/**/.gitkeep

*.wav
*.mp3
*.mp4
*.mov
*.mkv
```

---

## `.env.example`

Arquivo de exemplo para variáveis de ambiente.

Ele mostra quais variáveis o projeto pode usar sem expor dados sensíveis.

Exemplo:

```env
APP_ENV=development
WHISPER_MODEL=medium
INPUT_VIDEO=input/live_bruta.mp4
```

O arquivo real `.env` não deve ser enviado para o Git.

---

# Pastas de Entrada, Saída e Cache

## `input/`

Pasta onde ficam os vídeos brutos que serão processados.

Exemplo:

```txt
input/
└── live_bruta.mp4
```

Características:

* contém arquivos grandes;
* não deve ser versionada com vídeos reais;
* deve manter apenas `.gitkeep` no Git.

---

## `output/`

Pasta onde ficam os arquivos finais gerados pelo sistema.

```txt
output/
├── long/
├── shorts/
├── vertical/
└── subtitles/
```

Essa pasta representa o resultado final da edição.

---

## `output/long/`

Vídeos longos editados.

Objetivo:

* vídeos de 20 a 30 minutos;
* formato principal para YouTube;
* conteúdo com melhores momentos organizados.

Exemplo:

```txt
output/long/video_editado_01.mp4
```

---

## `output/shorts/`

Shorts gerados automaticamente.

Objetivo:

* vídeos curtos de 15 a 45 segundos;
* cortes rápidos;
* conteúdo de impacto;
* pensado para YouTube Shorts, TikTok e Reels.

Exemplo:

```txt
output/shorts/short_01.mp4
```

---

## `output/vertical/`

Versões verticais dos shorts.

Objetivo:

* formato 9:16;
* resolução comum de 1080x1920;
* pronto para plataformas mobile.

Exemplo:

```txt
output/vertical/short_01_vertical.mp4
```

---

## `output/subtitles/`

Legendas finais exportadas.

Pode conter:

* `.srt`;
* `.ass`;
* legendas específicas para vídeos longos;
* legendas específicas para shorts.

Exemplo:

```txt
output/subtitles/short_01.ass
```

---

## `cache/`

Pasta de arquivos intermediários.

A pasta `cache/` existe para evitar retrabalho.

Ela pode armazenar resultados de etapas anteriores, como áudio extraído, transcrição e highlights.

---

## `cache/audio/`

Áudios extraídos dos vídeos.

Exemplo:

```txt
cache/audio/live_bruta.wav
```

Usado pela etapa de transcrição.

---

## `cache/transcripts/`

Transcrições e legendas intermediárias.

Pode conter:

```txt
cache/transcripts/transcript.json
cache/transcripts/subtitles.srt
cache/transcripts/subtitles.ass
```

O `transcript.json` deve armazenar os trechos falados com tempo inicial, tempo final e texto.

---

## `cache/highlights/`

Momentos relevantes detectados automaticamente.

Exemplo:

```txt
cache/highlights/highlights.json
```

Um highlight pode conter:

```json
{
  "start": 1200.5,
  "end": 1235.2,
  "score": 0.87,
  "reason": "momento com reação forte e fala de impacto"
}
```

---

## `cache/edit_plans/`

Planos de edição gerados pela IA.

Essa é uma das pastas mais importantes do projeto.

Exemplo:

```txt
cache/edit_plans/edit_plan.json
```

O `edit_plan.json` define o que será renderizado.

Ele pode informar:

* quais trechos serão usados;
* duração dos shorts;
* trechos dos vídeos longos;
* zooms;
* efeitos sonoros;
* legendas;
* cortes;
* estilos.

---

# Assets

## `assets/`

Pasta para recursos usados durante a edição.

```txt
assets/
├── sfx/
├── fonts/
└── overlays/
```

---

## `assets/sfx/`

Efeitos sonoros.

Exemplos:

```txt
assets/sfx/impact.mp3
assets/sfx/vine_boom.mp3
assets/sfx/pop.mp3
```

Usado para aplicar efeitos em momentos de impacto, surpresa ou humor.

---

## `assets/fonts/`

Fontes usadas nas legendas.

Exemplos:

```txt
assets/fonts/Montserrat-Bold.ttf
assets/fonts/Anton.ttf
```

Usado para criar legendas mais fortes, visuais e adequadas a Shorts.

---

## `assets/overlays/`

Elementos visuais aplicados ao vídeo.

Exemplos:

```txt
assets/overlays/subscribe.png
assets/overlays/like.png
assets/overlays/logo.png
```

---

# Código-Fonte

## `src/`

Pasta principal do código Python.

Todo código reutilizável deve ficar dentro de `src/`.

O objetivo é evitar que o `main.py` fique grande demais.

---

## `src/__init__.py`

Indica que `src` é um pacote Python.

Isso permite imports como:

```python
from src.config.paths import INPUT_DIR
```

---

# Configuração

## `src/config/`

Pasta responsável por configurações globais do projeto.

```txt
src/config/
├── paths.py
└── settings.py
```

---

## `src/config/paths.py`

Centraliza os caminhos do projeto.

Exemplo de conteúdo:

```python
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"
CACHE_DIR = ROOT_DIR / "cache"

AUDIO_CACHE_DIR = CACHE_DIR / "audio"
TRANSCRIPTS_CACHE_DIR = CACHE_DIR / "transcripts"
HIGHLIGHTS_CACHE_DIR = CACHE_DIR / "highlights"
EDIT_PLANS_CACHE_DIR = CACHE_DIR / "edit_plans"

ASSETS_DIR = ROOT_DIR / "assets"
SFX_DIR = ASSETS_DIR / "sfx"
FONTS_DIR = ASSETS_DIR / "fonts"
OVERLAYS_DIR = ASSETS_DIR / "overlays"
```

Vantagem:

* evita caminhos espalhados pelo projeto;
* facilita manutenção;
* reduz erros com arquivos.

---

## `src/config/settings.py`

Centraliza configurações do sistema.

Exemplo:

```python
WHISPER_MODEL = "medium"
SHORT_MIN_DURATION = 15
SHORT_MAX_DURATION = 45
LONG_VIDEO_MIN_DURATION = 20 * 60
LONG_VIDEO_MAX_DURATION = 30 * 60
```

Pode futuramente ler variáveis do `.env`.

---

# Áudio

## `src/audio/`

Módulo de áudio.

```txt
src/audio/
└── extractor.py
```

---

## `src/audio/extractor.py`

Responsável por extrair áudio do vídeo de entrada.

Entrada:

```txt
input/live_bruta.mp4
```

Saída:

```txt
cache/audio/live_bruta.wav
```

Esse áudio será usado pela transcrição.

---

# Transcrição

## `src/transcription/`

Módulo de transcrição.

```txt
src/transcription/
└── whisper_transcriber.py
```

---

## `src/transcription/whisper_transcriber.py`

Responsável por transcrever o áudio utilizando IA.

Entrada:

```txt
cache/audio/live_bruta.wav
```

Saída:

```txt
cache/transcripts/transcript.json
```

O transcript deve conter texto e timestamps.

Exemplo:

```json
[
  {
    "start": 10.5,
    "end": 13.2,
    "text": "mano olha isso"
  }
]
```

---

# Legendas

## `src/subtitles/`

Módulo de legendas.

```txt
src/subtitles/
├── srt_generator.py
├── ass_generator.py
└── subtitle_renderer.py
```

---

## `src/subtitles/srt_generator.py`

Gera legendas no formato `.srt`.

O `.srt` é simples, compatível com várias plataformas e editores.

Exemplo:

```txt
1
00:00:10,500 --> 00:00:13,200
mano olha isso
```

---

## `src/subtitles/ass_generator.py`

Gera legendas no formato `.ass`.

O `.ass` permite mais estilização do que `.srt`.

Pode controlar:

* fonte;
* cor;
* posição;
* borda;
* sombra;
* tamanho;
* estilos diferentes por trecho.

É útil para Shorts e vídeos com legendas dinâmicas.

---

## `src/subtitles/subtitle_renderer.py`

Renderiza legendas diretamente no vídeo.

Responsabilidades:

* aplicar legendas `.ass` ao vídeo;
* gerar versão final com legenda queimada;
* usar FFmpeg ou outra biblioteca de renderização.

---

# Highlights

## `src/highlights/`

Módulo responsável por detectar melhores momentos.

```txt
src/highlights/
├── detector.py
└── scorer.py
```

---

## `src/highlights/detector.py`

Detecta candidatos a highlight.

Pode usar:

* palavras-chave;
* intensidade de fala;
* risadas;
* pausas;
* exclamações;
* contexto da transcrição.

Exemplo de palavras-chave:

```txt
mano
caraca
não acredito
que isso
clipa
olha isso
```

---

## `src/highlights/scorer.py`

Atribui pontuação aos highlights.

Exemplo:

```json
{
  "start": 1200,
  "end": 1230,
  "score": 0.91
}
```

Quanto maior o score, maior a chance do trecho virar short ou entrar em vídeo longo.

---

# Planejamento da Edição

## `src/planning/`

Módulo responsável por gerar o plano de edição.

```txt
src/planning/
└── edit_planner.py
```

---

## `src/planning/edit_planner.py`

Gera o `edit_plan.json`.

Entrada:

* transcrição;
* highlights;
* configurações.

Saída:

```txt
cache/edit_plans/edit_plan.json
```

Esse arquivo descreve a edição antes da renderização.

Ele pode conter:

```json
{
  "shorts": [
    {
      "id": "short_01",
      "start": 1200,
      "end": 1235,
      "score": 0.91,
      "actions": [
        {
          "type": "zoom",
          "start": 1205,
          "end": 1208,
          "intensity": 1.2
        }
      ]
    }
  ]
}
```

---

# Edição

## `src/editing/`

Módulo de montagem lógica dos vídeos.

```txt
src/editing/
├── long_video_builder.py
└── shorts_builder.py
```

---

## `src/editing/shorts_builder.py`

Monta a lógica dos Shorts.

Responsabilidades:

* selecionar trechos de 15 a 45 segundos;
* garantir duração mínima e máxima;
* organizar nomes dos arquivos;
* preparar cortes para renderização.

---

## `src/editing/long_video_builder.py`

Monta a lógica dos vídeos longos.

Responsabilidades:

* criar vídeos de 20 a 30 minutos;
* organizar sequência de trechos;
* evitar cortes sem contexto;
* priorizar highlights fortes.

---

# Renderização

## `src/rendering/`

Módulo responsável por gerar os arquivos finais de vídeo.

```txt
src/rendering/
├── ffmpeg_utils.py
├── video_renderer.py
└── verticalizer.py
```

---

## `src/rendering/ffmpeg_utils.py`

Centraliza funções relacionadas ao FFmpeg.

Exemplos de funções:

```python
cut_video()
merge_clips()
add_audio()
add_subtitles()
convert_to_vertical()
```

Vantagem:

* evita comandos FFmpeg espalhados;
* facilita manutenção;
* reduz duplicação.

---

## `src/rendering/video_renderer.py`

Renderiza os vídeos finais a partir do plano de edição.

Entrada:

```txt
cache/edit_plans/edit_plan.json
```

Saída:

```txt
output/shorts/
output/long/
```

---

## `src/rendering/verticalizer.py`

Converte vídeos horizontais para formato vertical.

Entrada:

```txt
output/shorts/short_01.mp4
```

Saída:

```txt
output/vertical/short_01_vertical.mp4
```

Objetivo:

* transformar vídeos em formato 9:16;
* preparar conteúdo para Shorts, TikTok e Reels.

---

# Utilitários

## `src/utils/`

Funções auxiliares usadas em vários módulos.

```txt
src/utils/
├── logger.py
├── file_utils.py
└── time_utils.py
```

---

## `src/utils/logger.py`

Configuração de logs.

Serve para exibir mensagens claras durante o pipeline.

Exemplo:

```txt
[INFO] Extraindo áudio...
[INFO] Transcrevendo áudio...
[INFO] Gerando highlights...
```

---

## `src/utils/file_utils.py`

Funções auxiliares para arquivos.

Exemplos:

```python
load_json()
save_json()
ensure_dir()
file_exists()
```

---

## `src/utils/time_utils.py`

Funções auxiliares para tempo.

Exemplos:

```python
seconds_to_srt_timestamp()
srt_timestamp_to_seconds()
format_duration()
```

---

# Testes

## `tests/`

Pasta de testes automatizados.

Objetivo:

* validar funções importantes;
* evitar regressões;
* garantir que mudanças futuras não quebrem o pipeline.

Exemplos futuros:

```txt
tests/test_time_utils.py
tests/test_highlight_scorer.py
tests/test_edit_plan.py
```

---

# Ambiente do VS Code

## `.vscode/`

Pasta de configuração local do editor.

```txt
.vscode/
├── settings.json
├── launch.json
└── extensions.json
```

---

## `.vscode/settings.json`

Configura o comportamento do VS Code no projeto.

Responsabilidades:

* definir interpretador Python;
* configurar Pylance;
* configurar Ruff;
* ativar formatação ao salvar;
* reconhecer imports do `src`.

---

## `.vscode/launch.json`

Configura execução e debug.

Permite rodar o projeto pelo botão de debug do VS Code.

---

## `.vscode/extensions.json`

Lista extensões recomendadas para quem abrir o projeto.

Exemplos:

* Python;
* Pylance;
* Ruff;
* GitLens;
* GitHub Copilot;
* dotenv.

---

# Extensões Recomendadas do VS Code

## Python

Extensão oficial para desenvolvimento Python no VS Code.

Usada para:

* selecionar interpretador;
* rodar scripts;
* depurar código;
* integrar testes.

---

## Pylance

Servidor de linguagem para Python.

Ajuda com:

* autocomplete;
* análise de tipos;
* erros de importação;
* navegação entre arquivos.

---

## Ruff

Ferramenta para lint e formatação Python.

Usada para:

* encontrar problemas no código;
* padronizar estilo;
* formatar automaticamente.

---

## Black Formatter

Formatador de código Python.

Pode ser usado como alternativa ou complemento ao Ruff.

---

## GitLens

Melhora a integração com Git.

Ajuda a ver:

* histórico de alterações;
* autores;
* commits;
* comparação entre versões.

---

## GitHub Copilot

Assistente de código com IA.

Ajuda a criar, completar e refatorar código.

---

## GitHub Copilot Chat

Permite conversar com o Copilot dentro do VS Code.

Útil para pedir explicações, refatorações e ajuda com bugs.

---

## dotenv

Melhora o suporte a arquivos `.env`.

---

## Error Lens

Mostra erros e avisos diretamente na linha do código.

---

# Dependências Python

## `faster-whisper`

Biblioteca para transcrição de áudio usando modelos Whisper otimizados.

Uso no projeto:

* converter fala em texto;
* gerar timestamps;
* alimentar legendas;
* alimentar detecção de highlights.

---

## `moviepy`

Biblioteca Python para edição de vídeo.

Uso no projeto:

* cortar vídeos;
* juntar clipes;
* manipular áudio;
* gerar versões intermediárias.

---

## `ffmpeg-python`

Interface Python para FFmpeg.

Uso no projeto:

* montar comandos FFmpeg;
* extrair áudio;
* renderizar vídeos;
* aplicar legendas;
* converter formatos.

---

## `python-dotenv`

Biblioteca para carregar variáveis de ambiente a partir de `.env`.

Uso no projeto:

* carregar configurações locais;
* definir modelo do Whisper;
* configurar caminhos;
* evitar dados sensíveis no código.

---

## `pydantic`

Biblioteca para validação de dados.

Uso no projeto:

* validar `transcript.json`;
* validar `highlights.json`;
* validar `edit_plan.json`;
* evitar dados malformados no pipeline.

---

## `rich`

Biblioteca para melhorar a saída no terminal.

Uso no projeto:

* logs bonitos;
* mensagens coloridas;
* progresso do pipeline;
* tabelas no terminal.

---

## `ruff`

Ferramenta de lint e formatação.

Uso no projeto:

* manter padrão de código;
* identificar erros simples;
* formatar arquivos Python.

---

## `pytest`

Framework de testes Python.

Uso no projeto:

* testar funções;
* validar módulos;
* evitar que mudanças quebrem o pipeline.

---

# Dependências Externas

## FFmpeg

Ferramenta externa essencial para manipulação de áudio e vídeo.

Uso no projeto:

* extrair áudio;
* cortar vídeos;
* aplicar legendas;
* converter formatos;
* renderizar arquivos finais.

O FFmpeg precisa estar instalado no sistema operacional.

---

# Tipos de Arquivos Usados

## `.py`

Arquivos Python.

Contêm o código principal do projeto.

---

## `.md`

Arquivos Markdown.

Usados para documentação.

Exemplos:

```txt
README.md
ESTRUTURA.md
```

---

## `.json`

Arquivos estruturados de dados.

Usados para:

* transcrições;
* highlights;
* planos de edição;
* metadados.

---

## `.srt`

Formato simples de legenda.

Compatível com várias plataformas.

---

## `.ass`

Formato avançado de legenda.

Permite estilos visuais mais complexos.

---

## `.mp4`

Formato principal de vídeo.

Usado para:

* live bruta;
* shorts;
* vídeos longos;
* versões finais.

---

## `.wav`

Formato de áudio sem compressão.

Usado como áudio intermediário para transcrição.

---

## `.mp3`

Formato de áudio compactado.

Usado principalmente para efeitos sonoros.

---

## `.env`

Arquivo de variáveis de ambiente.

Não deve ser versionado.

---

## `.gitkeep`

Arquivo vazio usado para manter pastas vazias no Git.

O Git não versiona pastas vazias por padrão, então o `.gitkeep` garante que a estrutura seja preservada.

---

# Fluxo Geral do Projeto

```txt
input/live_bruta.mp4
        │
        ▼
cache/audio/live_bruta.wav
        │
        ▼
cache/transcripts/transcript.json
        │
        ▼
cache/highlights/highlights.json
        │
        ▼
cache/edit_plans/edit_plan.json
        │
        ▼
output/shorts/
output/long/
output/vertical/
output/subtitles/
```

---

# Princípios da Estrutura

## Separação de responsabilidades

Cada pasta tem uma função clara.

Exemplo:

* áudio fica em `src/audio/`;
* transcrição fica em `src/transcription/`;
* legendas ficam em `src/subtitles/`;
* renderização fica em `src/rendering/`.

---

## Código modular

O projeto deve evitar arquivos gigantes.

Cada módulo deve resolver um problema específico.

---

## Cache reutilizável

Etapas pesadas, como transcrição, devem gerar arquivos reutilizáveis.

Assim, se a renderização falhar, não é necessário transcrever tudo novamente.

---

## Configuração centralizada

Caminhos e configurações devem ficar em:

```txt
src/config/
```

Isso evita valores espalhados pelo código.

---

## Preparado para evolução

A estrutura foi pensada para permitir melhorias futuras, como:

* detecção de emoção;
* análise visual;
* crop dinâmico;
* efeitos automáticos;
* geração de thumbnails;
* publicação automática.

---

# Resumo

Esta estrutura organiza o projeto em camadas claras:

```txt
Entrada
Análise
Planejamento
Edição
Renderização
Saída
```

Essa separação torna o projeto mais fácil de entender, manter, testar e evoluir.
