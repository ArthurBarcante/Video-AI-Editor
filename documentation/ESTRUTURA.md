# Estrutura Do Projeto

Este documento explica a organização do repositório e o papel de cada pasta e arquivo relevante. A ideia é que qualquer pessoa consiga abrir o projeto e entender onde cada responsabilidade fica.

## Raiz Do Projeto

`main.py`
: Ponto de entrada do pipeline. Ele chama as etapas em ordem: localizar vídeo, validar, extrair áudio, transcrever, gerar legendas, detectar highlights, analisar contexto, analisar emoções, gerar plano de edição, gerar títulos, gerar thumbnails, renderizar shorts, verticalizar shorts, renderizar vídeo longo e gerar o plano de publicação.

`README.md`
: Glossário das documentações e guia para rodar ou atualizar o projeto em outro computador.

`requirements.txt`
: Lista de dependências Python usadas pelo projeto.

`pytest.ini`
: Configuração do Pytest.

`pyrightconfig.json`
: Configuração de análise estática do Pyright.

`.env`
: Configuração local do projeto. Define ambiente, modelo Whisper, limites de shorts, scores mínimos e outras variáveis. Não deve ser usado como documentação pública de valores finais.

`.env.example`
: Modelo de configuração para criar um `.env` novo.

`.gitignore`
: Define arquivos e pastas que não devem entrar no Git.

## Pastas De Entrada, Cache, Assets E Saída

`input/`
: Onde a live bruta deve ser colocada. O leitor procura arquivos `.mp4` nessa pasta e usa o primeiro encontrado em ordem alfabética.

`cache/`
: Guarda arquivos intermediários para acelerar execuções futuras.

`cache/audio/`
: Recebe o áudio `.wav` extraído da live.

`cache/transcripts/`
: Recebe a transcrição em JSON gerada pelo Whisper.

`cache/highlights/`
: Recebe `highlights.json`, com trechos candidatos a cortes.

`cache/context/`
: Recebe `context.json`, com blocos semânticos agrupados por tempo e assunto.

`cache/emotions/`
: Recebe `emotions.json`, com emoção, score emocional e intensidade de áudio por segmento.

`cache/titles/`
: Recebe `titles.json`, com sugestões automáticas de títulos para shorts e vídeos longos.

`cache/publishing/`
: Recebe `publish_plan.json`, com metadados seguros de publicação para os vídeos finais.

`cache/edit_plans/`
: Recebe `edit_plan.json`, que descreve como os vídeos serão montados.

`cache/metadata/`
: Guarda metadados coletados dos vídeos quando usados.

`cache/video/`
: Área reservada para arquivos intermediários de vídeo.

`assets/`
: Biblioteca de recursos externos usados na edição.

`assets/sfx/`
: Biblioteca de efeitos sonoros. Exemplo atual: `pop.mp3`.

`assets/fonts/`
: Pasta reservada para fontes usadas em legendas ou renderizações.

`assets/overlays/`
: Pasta reservada para elementos visuais sobrepostos.

`output/`
: Guarda os resultados finais.

`output/shorts/`
: Shorts horizontais ou baseados no corte original.

`output/vertical/`
: Shorts convertidos para 9:16 com fundo blur.

`output/long/`
: Vídeos longos montados a partir dos melhores segmentos.

`output/subtitles/`
: Legendas `.srt` e `.ass`.

`output/thumbnails/`
: Miniaturas `.jpg` geradas automaticamente para shorts e vídeos longos. Também guarda frames intermediários em `output/thumbnails/frames/`.

## Documentação

`documentation/ROADMAP.md`
: Planejamento por fases. Mostra entregas, status e resultado esperado.

`documentation/ESTRUTURA.md`
: Este documento. Explica a arquitetura física do repositório.

`documentation/PROCESSOS/`
: Pasta com uma documentação operacional para cada etapa do pipeline, de validação do vídeo até plano de publicação.

## Código Fonte

`src/__init__.py`
: Marca `src` como pacote Python.

### `src/audio/`

`src/audio/__init__.py`
: Marca o módulo de áudio como pacote.

`src/audio/extractor.py`
: Extrai áudio do vídeo com FFmpeg. Gera WAV mono em 16 kHz em `cache/audio/`, formato usado pela transcrição e análise de intensidade.

### `src/config/`

`src/config/__init__.py`
: Marca o módulo de configuração como pacote.

`src/config/paths.py`
: Centraliza caminhos do projeto: `input`, `cache`, `output`, `assets` e subpastas. Também cria diretórios necessários com `ensure_project_dirs()`.

`src/config/settings.py`
: Lê variáveis do `.env` e define parâmetros do sistema, como modelo Whisper, score mínimo de highlight, duração dos shorts, quantidade máxima de shorts e tamanho vertical.

### `src/video/`

`src/video/reader.py`
: Lista vídeos em `input/` e retorna o primeiro `.mp4` encontrado.

`src/video/validator.py`
: Valida se o arquivo existe, é `.mp4`, não está vazio e possui streams de áudio e vídeo.

`src/video/metadata.py`
: Usa FFprobe para obter duração, tamanho, codecs, resolução e FPS.

`src/video/converter.py`
: Contém utilidades de conversão de vídeo usadas por testes e futuras etapas de render.

### `src/transcription/`

`src/transcription/whisper_transcriber.py`
: Carrega o Faster Whisper, transcreve o áudio e salva a transcrição JSON em `cache/transcripts/`.

`src/transcription/transcript_schema.py`
: Define os schemas Pydantic de transcrição e segmentos.

`src/transcription/text_cleaner.py`
: Normaliza textos transcritos antes de salvar os segmentos.

### `src/subtitles/`

`src/subtitles/srt_generator.py`
: Gera legenda `.srt` simples a partir da transcrição.

`src/subtitles/ass_generator.py`
: Gera legendas `.ass` em modo `short` e `long`. O modo short usa texto maior, quebra curta e destaque de palavras importantes.

`src/subtitles/line_breaker.py`
: Quebra linhas de legenda para manter leitura confortável.

`src/subtitles/word_highlighter.py`
: Destaca palavras importantes em ASS com cor e negrito.

`src/subtitles/subtitle_renderer.py`
: Área reservada para renderização de legendas diretamente no vídeo.

### `src/highlights/`

`src/highlights/detector.py`
: Lê a transcrição e o áudio, calcula energia por segmento, detecta risadas, calcula score e salva `highlights.json`.

`src/highlights/scorer.py`
: Define palavras-chave e heurísticas que somam pontos ao highlight.

`src/highlights/audio_intensity.py`
: Lê WAV e calcula energia RMS por trecho.

`src/highlights/laugh_detector.py`
: Detecta risadas por texto e por combinação de texto com intensidade.

`src/highlights/highlight_schema.py`
: Define o schema de um highlight.

### `src/context/`

`src/context/__init__.py`
: Marca o módulo de contexto como pacote.

`src/context/context_analyser.py`
: Gera `cache/context/context.json` a partir da transcrição. Agrupa segmentos, extrai palavras relevantes, infere tópico e calcula importância do bloco.

`src/context/context_schema.py`
: Define os schemas Pydantic de blocos de contexto e análise de contexto.

`src/context/semantic_analyzer.py`
: Contém termos relevantes, extração de keywords, inferência de tópico e cálculo de importância semântica.

`src/context/topic_grouper.py`
: Agrupa segmentos próximos da transcrição em blocos de contexto por intervalo de tempo.

### `src/emotion/`

`src/emotion/__init__.py`
: Marca o módulo de emoção como pacote.

`src/emotion/emotion_analyzer.py`
: Gera `cache/emotions/emotions.json` cruzando texto transcrito com intensidade de áudio.

`src/emotion/emotion_rules.py`
: Define palavras e regras para detectar surpresa, raiva, alegria e empolgação.

`src/emotion/emotion_schema.py`
: Define os schemas Pydantic da análise emocional.

### `src/planning/`

`src/planning/edit_planner.py`
: Gera o plano de edição completo. Carrega highlights, contexto e emoções; prioriza; planeja shorts e vídeos longos; e salva `edit_plan.json`.

`src/planning/edit_plan_schema.py`
: Define os schemas Pydantic do plano: ações, shorts, segmentos longos, vídeos longos e plano final.

`src/planning/highlight_prioritizer.py`
: Calcula `priority_score`, ajustando o score original com sinais como intensidade, risada, exclamação, palavras-chave, duração, contexto e emoção.

`src/planning/decision_engine.py`
: Decide se um highlight vira short, se entra no vídeo longo, qual estilo recebe e quais ações automáticas serão aplicadas.

`src/planning/shorts_planner.py`
: Seleciona os melhores highlights para shorts, expande a janela para duração mínima/máxima, cria título e adiciona estilo/ações.

`src/planning/long_video_planner.py`
: Seleciona highlights para o vídeo longo, adiciona contexto antes/depois, limita duração total e mantém ordem cronológica.

### `src/effects/`

`src/effects/zoom_effects.py`
: Identifica ações de zoom e monta o filtro FFmpeg de crop/scale para aplicar zoom no vídeo.

`src/effects/sfx_effects.py`
: Mapeia a biblioteca de SFX e resolve arquivos como `pop`, `impact`, `laugh` e `suspense`.

### `src/titles/`

`src/titles/__init__.py`
: Marca o módulo de títulos como pacote.

`src/titles/title_generator.py`
: Gera `cache/titles/titles.json` a partir do plano de edição, contexto e emoções.

`src/titles/title_rules.py`
: Define regras de limpeza, variações e score inicial de CTR para títulos.

`src/titles/title_schema.py`
: Define os schemas Pydantic da análise de títulos.

### `src/thumbnails/`

`src/thumbnails/__init__.py`
: Marca o módulo de thumbnails como pacote.

`src/thumbnails/frame_capture.py`
: Captura frames com FFmpeg em timestamps definidos pelo plano de edição.

`src/thumbnails/thumbnail_selector.py`
: Seleciona timestamps e ordena candidatos de thumbnails.

`src/thumbnails/thumbnail_generator.py`
: Cria thumbnails JPG, adiciona texto com Pillow e salva em `output/thumbnails/`.

### `src/publishing/`

`src/publishing/__init__.py`
: Marca o módulo de publicação como pacote.

`src/publishing/publish_schema.py`
: Define os schemas Pydantic do plano de publicação.

`src/publishing/publish_planner.py`
: Gera `cache/publishing/publish_plan.json` a partir dos vídeos finais em `output/shorts/` e `output/long/`.

`src/publishing/youtube_publisher.py`
: Placeholder seguro para futura integração com YouTube.

`src/publishing/tiktok_publisher.py`
: Placeholder seguro para futura integração com TikTok.

`src/publishing/instagram_publisher.py`
: Placeholder seguro para futura integração com Instagram.

`src/publishing/scheduler.py`
: Placeholder seguro para futuro agendamento real de publicações.

### `src/editing/`

`src/editing/shorts_builder.py`
: Renderiza shorts a partir do `edit_plan.json`. Aplica corte, zoom, SFX e exporta para `output/shorts/`.

`src/editing/long_video_builder.py`
: Corta segmentos do vídeo original, concatena em ordem e exporta o vídeo longo em `output/long/`.

### `src/rendering/`

`src/rendering/ffmpeg_utils.py`
: Centraliza execução de FFmpeg/FFprobe, valida ferramentas disponíveis e protege caminhos de saída dentro do projeto.

`src/rendering/verticalizer.py`
: Converte shorts para 9:16 com fundo blur e vídeo real centralizado.

`src/rendering/video_renderer.py`
: Placeholder para uma camada futura de renderização geral baseada no plano de edição.

### `src/utils/`

`src/utils/file_utils.py`
: Funções para ler/salvar JSON, criar diretórios e formatar caminhos relativos ao projeto.

`src/utils/logger.py`
: Configuração central de logs.

`src/utils/time_utils.py`
: Conversões de segundos para timestamps SRT e ASS.

`src/utils/cache_utils.py`
: Área de utilidades de cache para expansões futuras.

## Testes

`tests/`
: Contém testes automatizados do pipeline.

`tests/conftest.py`
: Fixtures compartilhadas, incluindo vídeos/áudios de amostra.

`tests/test_main_phase3.py`
: Teste integrado do fluxo principal.

`tests/test_*`
: Testes unitários dos módulos de áudio, vídeo, transcrição, legendas, highlights, contexto, emoção, planejamento, renderização, SFX e verticalização.
