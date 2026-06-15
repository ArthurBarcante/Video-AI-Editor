from pathlib import Path

from src.config.paths import OUTPUT_SHORTS_DIR
from src.config.paths import OUTPUT_VERTICAL_DIR
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.rendering.ffmpeg_utils import run_command
from src.utils.file_utils import format_project_path
from src.utils.logger import get_logger


logger = get_logger(__name__)


def verticalize_with_blur(
    input_path: str | Path,
    output_path: str | Path | None = None,
    width: int = 1080,
    height: int = 1920,
    force: bool = False,
) -> Path:
    input_path = Path(input_path)

    if output_path is None:
        output_path = OUTPUT_VERTICAL_DIR / f"{input_path.stem}_vertical.mp4"

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        logger.info("Vídeo vertical já existe: %s", format_project_path(output_path))
        return output_path

    logger.info("Verticalizando com fundo blur: %s", format_project_path(input_path))

    blur_width = max(width // 2, 1)
    blur_height = max(height // 2, 1)

    filter_complex = (
        f"[0:v]scale={blur_width}:{blur_height}:force_original_aspect_ratio=increase,"
        f"crop={blur_width}:{blur_height},boxblur=12:1,"
        f"scale={width}:{height}[bg];"
        f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
        "setsar=1[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-filter_complex",
        filter_complex,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    run_command(command)

    logger.info("Vídeo vertical gerado: %s", format_project_path(output_path))

    return output_path


def verticalize_all_shorts(
    shorts_dir: str | Path = OUTPUT_SHORTS_DIR,
    output_dir: str | Path = OUTPUT_VERTICAL_DIR,
    force: bool = False,
) -> list[Path]:
    shorts_dir = Path(shorts_dir)
    videos = sorted(shorts_dir.glob("*.mp4"))

    return verticalize_shorts(
        videos,
        output_dir=output_dir,
        force=force,
    )


def verticalize_shorts(
    short_paths: list[str | Path],
    output_dir: str | Path = OUTPUT_VERTICAL_DIR,
    force: bool = False,
) -> list[Path]:
    output_dir = Path(output_dir)

    rendered = []

    for video in sorted(Path(path) for path in short_paths):
        output_path = output_dir / f"{video.stem}_vertical.mp4"

        vertical_path = verticalize_with_blur(
            input_path=video,
            output_path=output_path,
            force=force,
        )

        rendered.append(vertical_path)

    logger.info("Shorts verticalizados: %s", len(rendered))

    return rendered
