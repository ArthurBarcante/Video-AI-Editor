from pathlib import Path

from src.config.paths import OUTPUT_SHORTS_DIR
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path, run_command
from src.utils.file_utils import format_project_path, load_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def render_short(
    source_video: str | Path,
    short: dict,
    output_dir: str | Path | None = None,
    force: bool = False,
) -> Path:
    source_video = Path(source_video)
    if output_dir is None:
        output_dir = OUTPUT_SHORTS_DIR

    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{short['id']}.mp4"
    ensure_safe_project_output_path(output_path)

    if output_path.exists() and not force:
        logger.info("Short já existe: %s", format_project_path(output_path))
        return output_path

    start = str(short["start"])
    duration = str(short["duration"])

    logger.info("Renderizando short: %s", short["id"])

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        start,
        "-i",
        str(source_video),
        "-t",
        duration,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    run_command(command)

    logger.info("Short exportado: %s", format_project_path(output_path))

    return output_path


def render_shorts_from_edit_plan(
    edit_plan_path: str | Path,
    force: bool = False,
) -> list[Path]:
    edit_plan = load_json(edit_plan_path)

    source_video = edit_plan["source_video"]
    shorts = edit_plan.get("shorts", [])

    rendered = []

    for short in shorts:
        output_path = render_short(
            source_video=source_video,
            short=short,
            force=force,
        )

        rendered.append(output_path)

    logger.info("Shorts renderizados: %s", len(rendered))

    return rendered
