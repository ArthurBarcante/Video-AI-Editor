from pathlib import Path

from src.video.metadata import get_video_streams


def validate_audio_file(audio_path: str | Path) -> Path:
    path = Path(audio_path)

    if not path.exists():
        raise FileNotFoundError(f"Áudio não encontrado: {path}")

    if not path.is_file():
        raise ValueError(f"O caminho não é um arquivo: {path}")

    if path.suffix.lower() != ".wav":
        raise ValueError(f"O arquivo de áudio não é .wav: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"O arquivo de áudio está vazio: {path}")

    streams_data = get_video_streams(path)
    streams = streams_data.get("streams", [])

    has_audio = any(stream.get("codec_type") == "audio" for stream in streams)

    if not has_audio:
        raise ValueError(f"O arquivo WAV não possui stream de áudio: {path}")

    return path
