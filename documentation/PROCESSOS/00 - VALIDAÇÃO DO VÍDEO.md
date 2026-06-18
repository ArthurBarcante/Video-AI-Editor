# 00 - Validação Do Vídeo

## Objetivo

Garantir que existe um vídeo bruto válido para o pipeline trabalhar.

## Onde Acontece

Arquivos principais:

```text
main.py
src/video/reader.py
src/video/validator.py
src/video/metadata.py
src/rendering/ffmpeg_utils.py
```

## Entrada

```text
input/*.mp4
```

Hoje o sistema aceita apenas arquivos `.mp4`. Se houver mais de um vídeo em `input/`, o sistema usa o primeiro em ordem alfabética.

## Saída

Não gera um arquivo próprio de cache nesta etapa principal. Ela devolve para o `main.py` o caminho do vídeo validado e um dicionário de metadados.

Metadados lidos:

```text
filename
duration
size_bytes
bitrate
video_codec
audio_codec
width
height
fps
```

## Como Atua Hoje

1. `get_first_input_video()` lista os arquivos em `input/`.
2. Filtra apenas arquivos com extensão `.mp4`.
3. Ordena os arquivos encontrados.
4. Seleciona o primeiro.
5. `validate_video_file()` verifica:
   - se o arquivo existe;
   - se é arquivo, não pasta;
   - se termina com `.mp4`;
   - se não está vazio;
   - se possui stream de vídeo;
   - se possui stream de áudio.
6. `get_video_metadata()` chama `ffprobe` e extrai duração, codecs, resolução, bitrate e FPS.

## Cache

Não usa cache direto. A validação roda em toda execução, porque é barata e evita processar arquivo inválido.

## Tempo Observado

Na execução limpa com vídeo de `57min21s`, esta etapa levou menos de `1s`.

## Gargalos

Baixo impacto. O custo é basicamente uma chamada ao `ffprobe`.

## Pontos De Otimização

Prioridade baixa.

Possíveis melhorias futuras:

- Aceitar seleção explícita de arquivo por argumento.
- Registrar metadados em `cache/metadata/` para auditoria.
- Aceitar outros formatos de entrada, como `.mkv`, `.mov` e `.webm`.
- Validar resolução e FPS mínimos antes de iniciar o pipeline.
