from pathlib import Path

from src.rendering.ffmpeg_utils import (
    ensure_safe_project_output_path,
    run_ffmpeg_command,
)
from src.utils.logger import get_logger


logger = get_logger(__name__)


def convert_to_mp4(
    input_path: str | Path,
    output_path: str | Path,
    force: bool = False,
) -> Path:
    input_path = Path(input_path)
    output_path = Path(output_path)

    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        logger.info("Vídeo convertido já existe em cache: %s", output_path)
        return output_path

    logger.info("Convertendo vídeo para MP4: %s", input_path)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    run_ffmpeg_command(command, error_label="conversão para MP4")

    logger.info("Vídeo convertido com sucesso: %s", output_path)

    return output_path


def resize_video(
    input_path: str | Path,
    output_path: str | Path,
    width: int = 1280,
    height: int = 720,
    force: bool = False,
) -> Path:
    input_path = Path(input_path)
    output_path = Path(output_path)

    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        logger.info("Vídeo redimensionado já existe em cache: %s", output_path)
        return output_path

    logger.info("Redimensionando vídeo para %sx%s", width, height)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vf",
        f"scale={width}:{height}",
        "-c:a",
        "copy",
        str(output_path),
    ]

    run_ffmpeg_command(command, error_label="redimensionamento de vídeo")

    logger.info("Vídeo redimensionado com sucesso: %s", output_path)

    return output_path


def convert_fps(
    input_path: str | Path,
    output_path: str | Path,
    fps: int = 30,
    force: bool = False,
) -> Path:
    input_path = Path(input_path)
    output_path = Path(output_path)

    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        logger.info("Vídeo com FPS convertido já existe em cache: %s", output_path)
        return output_path

    logger.info("Convertendo FPS para %s", fps)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-filter:v",
        f"fps={fps}",
        "-c:a",
        "copy",
        str(output_path),
    ]

    run_ffmpeg_command(command, error_label="conversão de FPS")

    logger.info("FPS convertido com sucesso: %s", output_path)

    return output_path


def cut_video_segment(
    input_path: str | Path,
    output_path: str | Path,
    start: str,
    end: str,
    force: bool = False,
) -> Path:
    input_path = Path(input_path)
    output_path = Path(output_path)

    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        logger.info("Trecho já existe em cache: %s", output_path)
        return output_path

    logger.info("Cortando trecho: %s até %s", start, end)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-ss",
        start,
        "-to",
        end,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    run_ffmpeg_command(command, error_label="corte de trecho de vídeo")

    logger.info("Trecho cortado com sucesso: %s", output_path)

    return output_path
