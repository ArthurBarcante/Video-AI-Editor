import subprocess
import time
from pathlib import Path

from src.audio.audio_validator import validate_audio_file
from src.audio.cache_signature import build_video_cache_signature
from src.audio.chunker import create_audio_chunks
from src.config.paths import CACHE_AUDIO_CHUNKS_DIR, CACHE_AUDIO_DIR
from src.config.settings import (
    AUDIO_CHANNELS,
    AUDIO_CHUNK_DURATION,
    AUDIO_CHUNK_OVERLAP,
    AUDIO_CODEC,
    AUDIO_CREATE_CHUNKS,
    AUDIO_FAST_TEST_MODE,
    AUDIO_SAMPLE_RATE,
    AUDIO_TEST_DURATION,
)
from src.rendering.ffmpeg_utils import (
    FFmpegError,
    ensure_safe_project_output_path,
    run_command,
)
from src.utils.file_utils import format_project_path, save_json
from src.utils.logger import get_logger

logger = get_logger(__name__)


def extract_audio_from_video(
    video_path: str | Path,
    output_dir: str | Path = CACHE_AUDIO_DIR,
    force: bool = False,
) -> Path:
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    cache_signature = build_video_cache_signature(video_path)

    ensure_safe_project_output_path(output_dir / f"{video_path.stem}_{cache_signature}.wav")
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_path = output_dir / f"{video_path.stem}_{cache_signature}.wav"
    metadata_path = output_dir / f"{video_path.stem}_{cache_signature}_audio_metadata.json"
    video_stat = video_path.stat()

    if audio_path.exists() and not force:
        logger.info("Áudio já existe em cache: %s", format_project_path(audio_path))
        validate_audio_file(audio_path)
        if AUDIO_CREATE_CHUNKS:
            create_audio_chunks(
                audio_path=audio_path,
                output_dir=CACHE_AUDIO_CHUNKS_DIR,
                chunk_duration=AUDIO_CHUNK_DURATION,
                overlap=AUDIO_CHUNK_OVERLAP,
                force=False,
            )
        return audio_path

    logger.info("Extraindo áudio de: %s", format_project_path(video_path))

    command = [
        "ffmpeg",
        "-y",
    ]

    if AUDIO_FAST_TEST_MODE:
        command.extend(["-t", str(AUDIO_TEST_DURATION)])

    command.extend(
        [
            "-i",
            str(video_path),
            "-map",
            "0:a:0",
            "-vn",
            "-acodec",
            AUDIO_CODEC,
            "-ar",
            str(AUDIO_SAMPLE_RATE),
            "-ac",
            str(AUDIO_CHANNELS),
            str(audio_path),
        ]
    )

    start_time = time.perf_counter()

    try:
        run_command(command)
    except subprocess.CalledProcessError as error:
        details = (error.stderr or error.stdout or "").strip()
        message = "Falha ao executar extração de áudio"
        if details:
            message = f"{message}: {details}"
        raise FFmpegError(message) from error

    elapsed = time.perf_counter() - start_time
    validate_audio_file(audio_path)
    chunks_metadata = None

    if AUDIO_CREATE_CHUNKS:
        chunks_metadata = create_audio_chunks(
            audio_path=audio_path,
            output_dir=CACHE_AUDIO_CHUNKS_DIR,
            chunk_duration=AUDIO_CHUNK_DURATION,
            overlap=AUDIO_CHUNK_OVERLAP,
            force=force,
        )

    metadata = {
        "source_video": format_project_path(video_path),
        "audio_path": format_project_path(audio_path),
        "cache_signature": cache_signature,
        "signature_strategy": "file_size_modified_time",
        "source_file_size_bytes": video_stat.st_size,
        "source_modified_time_ns": video_stat.st_mtime_ns,
        "execution_time_seconds": round(elapsed, 2),
        "sample_rate": AUDIO_SAMPLE_RATE,
        "channels": AUDIO_CHANNELS,
        "codec": AUDIO_CODEC,
        "file_size_bytes": audio_path.stat().st_size,
        "fast_test_mode": AUDIO_FAST_TEST_MODE,
        "test_duration_seconds": AUDIO_TEST_DURATION if AUDIO_FAST_TEST_MODE else None,
        "chunks_enabled": AUDIO_CREATE_CHUNKS,
        "chunks_metadata_path": chunks_metadata["metadata_path"]
        if chunks_metadata
        else None,
        "chunk_count": chunks_metadata["chunk_count"] if chunks_metadata else 0,
        "chunk_duration": AUDIO_CHUNK_DURATION if AUDIO_CREATE_CHUNKS else None,
        "chunk_overlap": AUDIO_CHUNK_OVERLAP if AUDIO_CREATE_CHUNKS else None,
    }

    save_json(metadata, metadata_path)

    logger.info("Áudio extraído com sucesso: %s", format_project_path(audio_path))
    logger.info("Tempo de extração: %.2fs", elapsed)
    logger.info("Tamanho do WAV: %.2f MB", audio_path.stat().st_size / (1024 * 1024))

    return audio_path
