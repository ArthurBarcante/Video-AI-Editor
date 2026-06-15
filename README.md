# Video AI Editor

Este repositório contém um pipeline de edição automática para transformar uma live bruta em conteúdos prontos para publicação: shorts, vídeos longos, legendas, zooms, efeitos sonoros e versões verticais.

Este `README.md` funciona como glossário das documentações do projeto e como guia rápido para levar o projeto para outro computador usando Git.

## Glossário Das Documentações

`documentation/ROADMAP.md`
: Lista as fases do projeto, o status de cada uma e os resultados esperados. Use este arquivo para saber o que já foi entregue e o que ainda está planejado.

`documentation/ESTRUTURA.md`
: Explica a estrutura do repositório em detalhes. Mostra o papel de cada pasta, página e arquivo importante do projeto.

`documentation/EXPLICAÇÕES/IA.md`
: Registra como a IA do projeto funciona hoje. Explica as heurísticas de highlights, priorização, planejamento de cortes, ações automáticas, SFX e verticalização.

`documentation/EXPLICAÇÕES/LÓGICAS.md`
: Explica o fluxo macro do sistema. É o melhor arquivo para entender como o `main.py` orquestra as etapas de entrada, análise, planejamento e renderização.

## Glossário Técnico Rápido

`input/`
: Pasta onde entra a live bruta em `.mp4`.

`cache/`
: Pasta de arquivos intermediários reutilizáveis, como áudio extraído, transcrição, highlights e plano de edição.

`output/`
: Pasta de resultados finais: shorts, vídeo longo, legendas e versões verticais.

`assets/`
: Biblioteca de recursos usados na edição, como efeitos sonoros, fontes e overlays.

`main.py`
: Ponto de entrada do sistema. Executa o pipeline completo.

`edit_plan.json`
: Plano de edição gerado automaticamente. Define shorts, vídeos longos, segmentos e ações como zoom e SFX.

`highlight`
: Trecho da live que recebeu score suficiente para ser considerado um bom momento.

`priority_score`
: Score ajustado usado para escolher os melhores highlights, sem depender apenas do score inicial.

`action`
: Ação de edição planejada para um short, como `zoom` ou `sfx`.

## Rodando O Projeto

1. Coloque um vídeo `.mp4` em `input/`.
2. Configure o `.env` com os parâmetros desejados.
3. Rode o pipeline:

```bash
./.venv/bin/python main.py
```

Neste ambiente, o comando `python main.py` pode não funcionar se `python` não existir no PATH. Usar `./.venv/bin/python main.py` evita esse problema.

## Passando O Projeto Para Outro Computador

No computador atual, salve as mudanças no Git e envie para o repositório remoto:

```bash
git status
git add .
git commit -m "Atualiza documentacao e pipeline"
git push
```

No outro computador, baixe ou atualize o projeto:

```bash
git clone <url-do-repositorio>
cd projeto_ai_editor
```

Se o projeto já existir nesse computador:

```bash
cd projeto_ai_editor
git pull
```

Depois prepare o ambiente:

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
cp .env.example .env
```

Também é necessário ter o FFmpeg instalado no sistema:

```bash
ffmpeg -version
ffprobe -version
```

Arquivos grandes, como vídeos em `input/`, saídas em `output/` e caches em `cache/`, podem não estar versionados. Se o outro computador precisar reproduzir exatamente o mesmo processamento, copie também os arquivos de mídia necessários.

## Saídas Esperadas

Após uma execução completa, o projeto pode gerar:

```text
cache/audio/
cache/transcripts/
cache/highlights/highlights.json
cache/edit_plans/edit_plan.json
output/subtitles/
output/shorts/
output/long/
output/vertical/
```

O arquivo mais importante para auditoria da edição é:

```text
cache/edit_plans/edit_plan.json
```

Ele mostra quais cortes foram escolhidos e quais ações automáticas serão aplicadas.
