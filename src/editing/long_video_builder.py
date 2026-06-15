import tempfile
from pathlib import Path

from src.config.paths import OUTPUT_LONG_DIR
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path, run_command
from src.utils.file_utils import format_project_path, load_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def cut_segment(
    source_video: str | Path,
    segment: dict,
    output_path: str | Path,
) -> Path:
    source_video = Path(source_video)
    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(segment["start"]),
        "-i",
        str(source_video),
        "-t",
        str(segment["duration"]),
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    run_command(command)

    return output_path


def concat_segments(segment_paths: list[Path], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    concat_file = output_path.parent / f"{output_path.stem}_concat.txt"

    lines = [
        f"file '{segment_path.resolve()}'"
        for segment_path in segment_paths
    ]

    concat_file.write_text("\n".join(lines), encoding="utf-8")

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(output_path),
    ]

    run_command(command)

    concat_file.unlink(missing_ok=True)

    return output_path


def render_long_video(
    source_video: str | Path,
    long_video: dict,
    output_dir: str | Path | None = None,
    force: bool = False,
) -> Path:
    source_video = Path(source_video)
    if output_dir is None:
        output_dir = OUTPUT_LONG_DIR

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{long_video['id']}.mp4"
    ensure_safe_project_output_path(output_path)

    if output_path.exists() and not force:
        logger.info("Vídeo longo já existe: %s", format_project_path(output_path))
        return output_path

    segments = long_video.get("segments", [])

    if not segments:
        raise ValueError(f"Nenhum segmento encontrado para {long_video['id']}")

    logger.info("Renderizando vídeo longo: %s", long_video["id"])

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        segment_paths = []

        for index, segment in enumerate(segments, start=1):
            segment_path = temp_dir / f"segment_{index:03}.mp4"

            cut_segment(
                source_video=source_video,
                segment=segment,
                output_path=segment_path,
            )

            segment_paths.append(segment_path)

        concat_segments(segment_paths, output_path)

    logger.info("Vídeo longo exportado: %s", format_project_path(output_path))

    return output_path


def render_long_videos_from_edit_plan(
    edit_plan_path: str | Path,
    force: bool = False,
) -> list[Path]:
    edit_plan = load_json(edit_plan_path)

    source_video = edit_plan["source_video"]
    long_videos = edit_plan.get("long_videos", [])

    rendered = []

    for long_video in long_videos:
        output_path = render_long_video(
            source_video=source_video,
            long_video=long_video,
            force=force,
        )

        rendered.append(output_path)

    logger.info("Vídeos longos renderizados: %s", len(rendered))

    return rendered
