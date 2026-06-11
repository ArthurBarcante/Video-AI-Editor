from pathlib import Path

from src.config.paths import OUTPUT_SUBTITLES_DIR
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.transcription.transcript_schema import Transcript
from src.utils.file_utils import format_project_path, load_json
from src.utils.logger import get_logger
from src.utils.time_utils import seconds_to_srt_timestamp


logger = get_logger(__name__)


def generate_srt(
    transcript_path: str | Path,
    output_path: str | Path | None = None,
) -> Path:
    transcript_path = Path(transcript_path)
    transcript = Transcript.model_validate(load_json(transcript_path))

    if output_path is None:
        output_path = OUTPUT_SUBTITLES_DIR / f"{transcript_path.stem}.srt"

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    for index, segment in enumerate(transcript.segments, start=1):
        start = seconds_to_srt_timestamp(segment.start)
        end = seconds_to_srt_timestamp(segment.end)
        text = segment.text

        lines.append(f"{index}")
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")

    logger.info("Legenda SRT gerada em: %s", format_project_path(output_path))

    return output_path
