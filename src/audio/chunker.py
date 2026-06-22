import subprocess
import time
from pathlib import Path

from src.audio.audio_validator import validate_audio_file
from src.config.paths import CACHE_AUDIO_CHUNKS_DIR
from src.config.settings import (
    AUDIO_CHANNELS,
    AUDIO_CHUNK_DURATION,
    AUDIO_CHUNK_OVERLAP,
    AUDIO_CODEC,
    AUDIO_SAMPLE_RATE,
)
from src.rendering.ffmpeg_utils import FFmpegError, run_command
from src.utils.file_utils import format_project_path, save_json
from src.video.metadata import get_video_metadata


def build_audio_chunk_ranges(
    audio_duration: float,
    chunk_duration: int = AUDIO_CHUNK_DURATION,
    overlap: int = AUDIO_CHUNK_OVERLAP,
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

    try:
        run_command(command)
    except subprocess.CalledProcessError as error:
        details = (error.stderr or error.stdout or "").strip()
        message = "Falha ao criar chunk de áudio"
        if details:
            message = f"{message}: {details}"
        raise FFmpegError(message) from error

    validate_audio_file(output_path)

    return output_path


def create_audio_chunks(
    audio_path: str | Path,
    output_dir: str | Path = CACHE_AUDIO_CHUNKS_DIR,
    chunk_duration: int = AUDIO_CHUNK_DURATION,
    overlap: int = AUDIO_CHUNK_OVERLAP,
    force: bool = False,
) -> dict:
    audio_path = Path(audio_path)
    output_dir = Path(output_dir)
    audio_duration = float(get_video_metadata(audio_path)["duration"])
    chunk_ranges = build_audio_chunk_ranges(
        audio_duration=audio_duration,
        chunk_duration=chunk_duration,
        overlap=overlap,
    )
    chunk_dir = output_dir / audio_path.stem / f"duration_{chunk_duration}_overlap_{overlap}"
    chunk_dir.mkdir(parents=True, exist_ok=True)

    started_at = time.perf_counter()
    chunks = []
    reused_count = 0

    for chunk in chunk_ranges:
        chunk_path = chunk_dir / f"{audio_path.stem}_chunk_{chunk['index']:03}.wav"

        if chunk_path.exists() and not force:
            validate_audio_file(chunk_path)
            reused = True
            reused_count += 1
        else:
            create_audio_chunk(
                audio_path=audio_path,
                output_path=chunk_path,
                start=chunk["start"],
                duration=chunk["duration"],
            )
            reused = False

        chunks.append(
            {
                "index": chunk["index"],
                "start": chunk["start"],
                "end": chunk["end"],
                "duration": chunk["duration"],
                "path": format_project_path(chunk_path),
                "file_size_bytes": chunk_path.stat().st_size,
                "reused_from_cache": reused,
            }
        )

    elapsed = time.perf_counter() - started_at
    metadata = {
        "source_audio": format_project_path(audio_path),
        "chunks_dir": format_project_path(chunk_dir),
        "audio_duration_seconds": audio_duration,
        "chunk_duration": chunk_duration,
        "chunk_overlap": overlap,
        "chunk_count": len(chunks),
        "chunks_reused_from_cache": reused_count,
        "execution_time_seconds": round(elapsed, 2),
        "chunks": chunks,
    }
    metadata_path = chunk_dir / "chunks_metadata.json"
    save_json(metadata, metadata_path)
    metadata["metadata_path"] = format_project_path(metadata_path)

    return metadata
