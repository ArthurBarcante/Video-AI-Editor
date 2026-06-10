# Comandos do Projeto

Este documento reúne os comandos mais importantes utilizados durante o desenvolvimento do Video AI Editor.

---

# Ambiente Virtual

## Criar ambiente virtual

Linux/macOS

```bash
python3 -m venv .venv
```

Windows

```powershell
python -m venv .venv
```

---

## Ativar ambiente virtual

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

---

## Desativar ambiente virtual

```bash
deactivate
```

---

# Dependências

## Atualizar pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Gerar requirements.txt

```bash
pip freeze > requirements.txt
```

---

## Ver dependências instaladas

```bash
pip list
```

---

# Execução do Projeto

## Executar pipeline principal

```bash
python main.py
```

Este comando executa o fluxo principal do sistema.

Fluxo esperado:

```text
Vídeo de entrada
↓
Extração de áudio
↓
Transcrição
↓
Geração de legendas
↓
Detecção de highlights
↓
Plano de edição
↓
Renderização
↓
Vídeos finais
```

---

# Testes

## Executar todos os testes

```bash
pytest
```

---

## Executar um teste específico

```bash
pytest tests/test_highlights.py
```

---

## Executar testes com detalhes

```bash
pytest -v
```

---

# Ruff

## Verificar problemas no código

```bash
ruff check .
```

---

## Corrigir problemas automaticamente

```bash
ruff check . --fix
```

---

## Formatar projeto

```bash
ruff format .
```

---

# Git

## Verificar status

```bash
git status
```

---

## Adicionar alterações

```bash
git add .
```

---

## Criar commit

```bash
git commit -m "mensagem do commit"
```

Exemplo:

```bash
git commit -m "feat: adiciona transcrição inicial"
```

---

## Ver histórico

```bash
git log --oneline
```

---

## Enviar para GitHub

```bash
git push
```

---

## Baixar alterações

```bash
git pull
```

---

# Branches

## Criar branch

```bash
git checkout -b nome-da-branch
```

Exemplo:

```bash
git checkout -b feature/highlights
```

---

## Trocar branch

```bash
git checkout main
```

---

## Listar branches

```bash
git branch
```

---

# FFmpeg

## Verificar instalação

```bash
ffmpeg -version
```

---

## Extrair áudio de um vídeo

```bash
ffmpeg -i input/live.mp4 cache/audio/live.wav
```

---

## Converter vídeo

```bash
ffmpeg -i input.mp4 output.mp4
```

---

## Cortar trecho de vídeo

```bash
ffmpeg -i input.mp4 -ss 00:05:00 -to 00:05:30 output.mp4
```

---

## Gerar vídeo sem áudio

```bash
ffmpeg -i input.mp4 -an output.mp4
```

---

## Gerar áudio sem vídeo

```bash
ffmpeg -i input.mp4 -vn audio.wav
```

---

## Adicionar legenda ASS

```bash
ffmpeg -i input.mp4 -vf "ass=subtitles.ass" output.mp4
```

---

# Estrutura do Projeto

## Mostrar árvore de arquivos

Linux

```bash
tree
```

Caso não exista:

```bash
sudo apt install tree
```

---

## Mostrar árvore limitada

```bash
tree -L 2
```

---

# Python

## Executar módulo

```bash
python -m src.transcription.whisper_transcriber
```

---

## Ver versão do Python

```bash
python --version
```

---

## Ver caminho do Python

```bash
which python
```

Windows

```powershell
where python
```

---

# Variáveis de Ambiente

## Copiar arquivo de exemplo

Linux/macOS

```bash
cp .env.example .env
```

Windows

```powershell
copy .env.example .env
```

---

# VS Code

## Abrir projeto

```bash
code .
```

---

## Abrir pasta específica

```bash
code caminho/do/projeto
```

---

# Futuros Comandos do Projeto

Conforme o sistema evoluir, estes comandos deverão ser adicionados.

---

## Transcrever vídeo

```bash
python main.py transcribe
```

---

## Detectar highlights

```bash
python main.py highlights
```

---

## Gerar plano de edição

```bash
python main.py plan
```

---

## Gerar shorts

```bash
python main.py shorts
```

---

## Gerar vídeo longo

```bash
python main.py long
```

---

## Renderizar tudo

```bash
python main.py render
```

---

## Pipeline completo

```bash
python main.py all
```

---

# Comandos Mais Utilizados

Durante o desenvolvimento, os comandos mais frequentes serão:

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

```bash
ruff check .
```

```bash
ruff format .
```

```bash
pytest
```

```bash
git status
```

```bash
git add .
```

```bash
git commit -m "mensagem"
```

```bash
git push
```

---

# Resumo

Fluxo diário típico:

```text
Ativar ambiente
↓
Atualizar código
↓
Desenvolver
↓
Rodar testes
↓
Executar pipeline
↓
Commit
↓
Push
```

Esse será o ciclo principal de desenvolvimento do projeto.
