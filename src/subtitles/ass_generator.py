from pathlib import Path

from src.config.paths import OUTPUT_SUBTITLES_DIR
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.transcription.transcript_schema import Transcript
from src.utils.file_utils import format_project_path, load_json
from src.utils.logger import get_logger
from src.utils.time_utils import seconds_to_ass_timestamp


logger = get_logger(__name__)


ASS_HEADER = """[Script Info]
Title: Video AI Editor Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,64,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,4,2,2,40,40,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def generate_ass(
    transcript_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
) -> Path:
    transcript_path = Path(transcript_path)

    if output_path is None:
        output_path = OUTPUT_SUBTITLES_DIR / f"{transcript_path.stem}.ass"

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        logger.info("Legenda ASS já existe em cache: %s", format_project_path(output_path))
        return output_path

    transcript = Transcript.model_validate(load_json(transcript_path))

    events = []

    for segment in transcript.segments:
        start = seconds_to_ass_timestamp(segment.start)
        end = seconds_to_ass_timestamp(segment.end)
        text = segment.text.replace("\n", " ")

        events.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")

    output_path.write_text(
        ASS_HEADER + "\n".join(events),
        encoding="utf-8",
    )

    logger.info("Legenda ASS gerada em: %s", format_project_path(output_path))

    return output_path
