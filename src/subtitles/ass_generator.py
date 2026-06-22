from pathlib import Path

from src.config.paths import OUTPUT_SUBTITLES_DIR
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.subtitles.line_breaker import break_subtitle_text
from src.transcription.subtitle_cleaner import prepare_subtitle_segments
from src.transcription.transcript_schema import Transcript
from src.utils.file_utils import format_project_path, load_json
from src.utils.logger import get_logger
from src.utils.time_utils import seconds_to_ass_timestamp


logger = get_logger(__name__)


ASS_HEADERS = {
    "short": """[Script Info]
Title: Video AI Editor Shorts Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Montserrat ExtraBold,70,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,0,2,70,70,170,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""",
    "long": """[Script Info]
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
""",
}

MODE_LINE_LIMITS = {
    "short": 42,
    "long": 42,
}


def _get_output_path(transcript_path: Path, mode: str) -> Path:
    return OUTPUT_SUBTITLES_DIR / f"{transcript_path.stem}_{mode}.ass"


def _format_text(text: str, mode: str) -> str:
    return break_subtitle_text(
        text.replace("\n", " "),
        max_chars_per_line=MODE_LINE_LIMITS[mode],
        max_lines=2,
    )


def _write_ass_file(
    transcript: Transcript,
    output_path: Path,
    mode: str,
    window_start: float | None = None,
    window_end: float | None = None,
) -> Path:
    segments = prepare_subtitle_segments(
        transcript.segments,
        window_start=window_start,
        window_end=window_end,
    )
    events = []

    for segment in segments:
        start = seconds_to_ass_timestamp(segment.start)
        end = seconds_to_ass_timestamp(segment.end)
        text = _format_text(segment.text, mode)

        events.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")

    output_path.write_text(
        ASS_HEADERS[mode] + "\n".join(events),
        encoding="utf-8",
    )

    return output_path


def generate_ass(
    transcript_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
    mode: str = "long",
) -> Path:
    transcript_path = Path(transcript_path)

    if mode not in ASS_HEADERS:
        valid_modes = ", ".join(sorted(ASS_HEADERS))
        raise ValueError(f"Modo ASS inválido: {mode}. Use: {valid_modes}")

    if output_path is None:
        output_path = _get_output_path(transcript_path, mode)

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        logger.info("Legenda ASS já existe em cache: %s", format_project_path(output_path))
        return output_path

    transcript = Transcript.model_validate(load_json(transcript_path))

    _write_ass_file(
        transcript=transcript,
        output_path=output_path,
        mode=mode,
    )

    logger.info("Legenda ASS gerada em: %s", format_project_path(output_path))

    return output_path


def generate_short_ass_files(
    transcript_path: str | Path,
    edit_plan_path: str | Path,
    output_dir: str | Path | None = None,
    force: bool = False,
) -> list[Path]:
    from src.subtitles.short_subtitle_generator import (
        generate_short_ass_files as generate_files,
    )

    return generate_files(
        transcript_path=transcript_path,
        edit_plan_path=edit_plan_path,
        output_dir=output_dir,
        force=force,
    )
