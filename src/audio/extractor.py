from pathlib import Path

from src.config.paths import CACHE_AUDIO_DIR, ROOT_DIR
from src.rendering.ffmpeg_utils import (
    ensure_safe_project_output_path,
    run_ffmpeg_command,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def format_project_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT_DIR))
    except ValueError:
        return str(path)


def extract_audio_from_video(
    video_path: str | Path,
    output_dir: str | Path = CACHE_AUDIO_DIR,
    sample_rate: int = 16000,
    force: bool = False,
) -> Path:
    video_path = Path(video_path)
    output_dir = Path(output_dir)

    ensure_safe_project_output_path(output_dir / f"{video_path.stem}.wav")
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_path = output_dir / f"{video_path.stem}.wav"

    if audio_path.exists() and not force:
        logger.info("Áudio já existe em cache: %s", format_project_path(audio_path))
        return audio_path

    logger.info("Extraindo áudio de: %s", format_project_path(video_path))

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        str(sample_rate),
        "-ac",
        "1",
        str(audio_path),
    ]

    run_ffmpeg_command(command, error_label="extração de áudio")

    logger.info("Áudio extraído com sucesso: %s", format_project_path(audio_path))

    return audio_path
