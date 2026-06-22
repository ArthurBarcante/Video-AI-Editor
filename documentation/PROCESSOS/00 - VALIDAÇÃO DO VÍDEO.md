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
src/video/validation_metadata.py
src/rendering/ffmpeg_utils.py
```

## Entrada

```text
input/*.mp4
python main.py input/live_01.mp4
python main.py --video input/live_01.mp4
```

Hoje o sistema aceita apenas arquivos `.mp4`.

Se um vídeo for passado por argumento posicional ou por `--video`, esse arquivo é usado.

Se nenhum caminho explícito for informado e houver mais de um vídeo em `input/`, o sistema usa o primeiro em ordem alfabética.

## Saída

```text
cache/metadata/<nome_do_video>_validation_metadata.json
```

A etapa gera metadata de auditoria da validação e devolve para o `main.py` o caminho do vídeo validado e um dicionário de metadados.

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

Metadata salva:

```json
{
  "file_name": "live_bruta.mp4",
  "source_path": "input/live_bruta.mp4",
  "duration": 3441.19,
  "width": 1920,
  "height": 1080,
  "fps": 60,
  "codec": "h264",
  "audio_codec": "aac",
  "bitrate": 2500000,
  "file_size_bytes": 1234567890,
  "validated_at": "2026-06-22T15:30:00-03:00"
}
```

## Como Atua Hoje

1. `main.py` lê os argumentos do terminal.
2. Se existir caminho explícito, usa esse vídeo.
3. Se não existir caminho explícito, `get_first_input_video()` lista os arquivos em `input/`.
4. Filtra apenas arquivos com extensão `.mp4`.
5. Ordena os arquivos encontrados.
6. Seleciona o primeiro.
7. `validate_video_file()` verifica:
   - se o arquivo existe;
   - se é arquivo, não pasta;
   - se termina com `.mp4`;
   - se não está vazio;
   - se possui stream de vídeo;
   - se possui stream de áudio.
8. `get_video_metadata()` chama `ffprobe` e extrai duração, codecs, resolução, bitrate e FPS.
9. `save_validation_metadata()` salva a metadata em `cache/metadata/`.

## Cache e Auditoria

Não usa cache para pular validação. A validação roda em toda execução, porque é barata e evita processar arquivo inválido.

A etapa salva um JSON em `cache/metadata/` para auditoria, debug e relatórios futuros.

## Tempo Observado

Na execução limpa com vídeo de `57min21s`, esta etapa levou menos de `1s`.

## Gargalos

Baixo impacto. O custo é basicamente uma chamada ao `ffprobe`.

## Pontos De Otimização

Prioridade baixa.

Possíveis melhorias futuras:

- Aceitar seleção explícita de arquivo por argumento. (**Feito**)
- Registrar metadados em `cache/metadata/` para auditoria. (**Feito**)
- Aceitar outros formatos de entrada, como `.mkv`, `.mov` e `.webm`.
- Avisar sobre resolução e FPS abaixo do recomendado sem bloquear o pipeline.
