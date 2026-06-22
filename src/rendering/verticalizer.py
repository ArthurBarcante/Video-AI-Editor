import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from src.config.paths import OUTPUT_SHORTS_DIR, OUTPUT_VERTICAL_DIR
from src.config.settings import (
    VERTICAL_BLUR_ENABLED,
    VERTICAL_FAST_HEIGHT,
    VERTICAL_FAST_MODE,
    VERTICAL_FAST_WIDTH,
    VERTICAL_HEIGHT,
    VERTICAL_RENDER_PARALLEL,
    VERTICAL_RENDER_PROFILE,
    VERTICAL_RENDER_WORKERS,
    VERTICAL_WIDTH,
)
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.rendering.ffmpeg_utils import run_command
from src.rendering.render_profiles import get_render_profile
from src.utils.cache_metadata import is_cache_valid, save_cache_metadata
from src.utils.file_utils import format_project_path
from src.utils.logger import get_logger


logger = get_logger(__name__)


def build_vertical_filter(width: int, height: int, blur_enabled: bool = True) -> str:
    if blur_enabled:
        return (
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},boxblur=20:1[bg];"
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2"
        )

    return (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
    )


def verticalize_with_blur(
    input_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
) -> Path:
    started_at = time.perf_counter()
    profile = get_render_profile(VERTICAL_RENDER_PROFILE)
    input_path = Path(input_path)

    if output_path is None:
        output_path = OUTPUT_VERTICAL_DIR / f"{input_path.stem}_vertical.mp4"

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cache_sources = [input_path]

    if output_path.exists() and not force and is_cache_valid(output_path, cache_sources):
        logger.info("Vídeo vertical já existe: %s", format_project_path(output_path))
        return output_path

    logger.info("Verticalizando com fundo blur: %s", format_project_path(input_path))

    render_width = VERTICAL_FAST_WIDTH if VERTICAL_FAST_MODE else VERTICAL_WIDTH
    render_height = VERTICAL_FAST_HEIGHT if VERTICAL_FAST_MODE else VERTICAL_HEIGHT
    filter_complex = build_vertical_filter(
        width=render_width,
        height=render_height,
        blur_enabled=VERTICAL_BLUR_ENABLED,
    )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
    ]

    if VERTICAL_BLUR_ENABLED:
        command.extend(["-filter_complex", filter_complex])
    else:
        command.extend(["-vf", filter_complex])

    command.extend(
        [
        "-c:v",
        profile["video_codec"],
        "-preset",
        profile["preset"],
        "-crf",
        profile["crf"],
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(output_path),
        ]
    )

    run_command(command)
    save_cache_metadata(output_path, cache_sources)
    elapsed = time.perf_counter() - started_at

    logger.info("Vídeo vertical gerado: %s", format_project_path(output_path))
    logger.info(
        "Vertical %s gerado em %.2fs usando perfil %s",
        input_path.name,
        elapsed,
        VERTICAL_RENDER_PROFILE,
    )

    return output_path


def verticalize_all_shorts(
    shorts_dir: str | Path = OUTPUT_SHORTS_DIR,
    output_dir: str | Path = OUTPUT_VERTICAL_DIR,
    force: bool = False,
) -> list[Path]:
    shorts_dir = Path(shorts_dir)
    output_dir = Path(output_dir)
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
    videos = sorted(Path(path) for path in short_paths)

    if not videos:
        logger.warning("Nenhum short encontrado para verticalizar.")
        return []

    started_at = time.perf_counter()

    if not VERTICAL_RENDER_PARALLEL or VERTICAL_RENDER_WORKERS <= 1:
        rendered = [
            verticalize_with_blur(
                input_path=video,
                output_path=output_dir / f"{video.stem}_vertical.mp4",
                force=force,
            )
            for video in videos
        ]
    else:
        rendered = []
        workers = min(VERTICAL_RENDER_WORKERS, len(videos))

        logger.info(
            "Verticalizando shorts em paralelo com %s workers",
            workers,
        )

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(
                    verticalize_with_blur,
                    input_path=video,
                    output_path=output_dir / f"{video.stem}_vertical.mp4",
                    force=force,
                )
                for video in videos
            ]

            for future in as_completed(futures):
                rendered.append(future.result())

        rendered = sorted(rendered)

    elapsed = time.perf_counter() - started_at

    logger.info("Shorts verticalizados: %s", len(rendered))
    logger.info("Tempo total verticalização: %.2fs", elapsed)

    return rendered
