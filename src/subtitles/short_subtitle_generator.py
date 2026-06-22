from pathlib import Path

from src.config.paths import OUTPUT_SUBTITLES_DIR
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.subtitles.ass_generator import ASS_HEADERS, _format_text
from src.subtitles.subtitle_segmenter import get_segments_for_range
from src.transcription.transcript_schema import Transcript
from src.utils.cache_metadata import is_cache_valid, save_cache_metadata
from src.utils.file_utils import format_project_path, load_json
from src.utils.logger import get_logger
from src.utils.time_utils import seconds_to_ass_timestamp


logger = get_logger(__name__)


def _write_short_ass(
    transcript: Transcript,
    short: dict,
    output_path: Path,
) -> Path:
    segments = get_segments_for_range(
        transcript=transcript,
        start=short["start"],
        end=short["end"],
    )
    events = []

    for segment in segments:
        start = seconds_to_ass_timestamp(segment.start)
        end = seconds_to_ass_timestamp(segment.end)
        text = _format_text(segment.text, "short")

        events.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")

    output_path.write_text(
        ASS_HEADERS["short"] + "\n".join(events),
        encoding="utf-8",
    )

    return output_path


def generate_short_ass_files(
    transcript_path: str | Path,
    edit_plan_path: str | Path,
    output_dir: str | Path | None = None,
    force: bool = False,
) -> list[Path]:
    transcript_path = Path(transcript_path)
    edit_plan_path = Path(edit_plan_path)

    if output_dir is None:
        output_dir = OUTPUT_SUBTITLES_DIR

    output_dir = Path(output_dir)
    ensure_safe_project_output_path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    transcript = Transcript.model_validate(load_json(transcript_path))
    edit_plan = load_json(edit_plan_path)

    output_paths = []

    for short in edit_plan.get("shorts", []):
        output_path = output_dir / f"{short['id']}.ass"
        ensure_safe_project_output_path(output_path)
        cache_sources = [transcript_path, edit_plan_path]

        if output_path.exists() and not force and is_cache_valid(output_path, cache_sources):
            logger.info(
                "Legenda ASS do short já existe em cache: %s",
                format_project_path(output_path),
            )
            output_paths.append(output_path)
            continue

        _write_short_ass(
            transcript=transcript,
            short=short,
            output_path=output_path,
        )
        save_cache_metadata(output_path, cache_sources)

        logger.info("Legenda ASS do short gerada em: %s", format_project_path(output_path))
        output_paths.append(output_path)

    return output_paths
