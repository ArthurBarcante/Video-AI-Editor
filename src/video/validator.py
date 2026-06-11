from pathlib import Path

from src.video.metadata import get_video_streams


def validate_video_file(video_path: str | Path) -> Path:
    path = Path(video_path)

    if not path.exists():
        raise FileNotFoundError(f"Vídeo não encontrado: {path}")

    if not path.is_file():
        raise ValueError(f"O caminho não é um arquivo: {path}")

    if path.suffix.lower() != ".mp4":
        raise ValueError(f"O arquivo não é .mp4: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"O arquivo está vazio: {path}")

    streams_data = get_video_streams(path)
    streams = streams_data.get("streams", [])

    has_video = any(stream.get("codec_type") == "video" for stream in streams)
    has_audio = any(stream.get("codec_type") == "audio" for stream in streams)

    if not has_video:
        raise ValueError(f"O arquivo não possui stream de vídeo: {path}")

    if not has_audio:
        raise ValueError(f"O arquivo não possui stream de áudio: {path}")

    return path