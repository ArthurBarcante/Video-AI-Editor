from pathlib import Path

from src.config.settings import AUDIO_CHANNELS, AUDIO_CODEC, AUDIO_SAMPLE_RATE
from src.rendering.ffmpeg_utils import run_command


def create_audio_chunk(
    audio_path: str | Path,
    output_path: str | Path,
    start: float,
    duration: float,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start),
        "-i",
        str(audio_path),
        "-t",
        str(duration),
        "-acodec",
        AUDIO_CODEC,
        "-ar",
        str(AUDIO_SAMPLE_RATE),
        "-ac",
        str(AUDIO_CHANNELS),
        str(output_path),
    ]

    run_command(command)

    return output_path


def build_chunk_ranges(
    audio_duration: float,
    chunk_duration: int,
    overlap: int,
) -> list[dict]:
    if audio_duration <= 0:
        return []

    if chunk_duration <= 0:
        raise ValueError("chunk_duration deve ser maior que zero")

    if overlap < 0:
        raise ValueError("overlap não pode ser negativo")

    if overlap >= chunk_duration:
        raise ValueError("overlap deve ser menor que chunk_duration")

    chunks = []
    start = 0.0
    index = 1

    while start < audio_duration:
        end = min(start + chunk_duration, audio_duration)

        chunks.append(
            {
                "index": index,
                "start": round(start, 3),
                "end": round(end, 3),
                "duration": round(end - start, 3),
            }
        )

        if end >= audio_duration:
            break

        start = end - overlap
        index += 1

    return chunks
