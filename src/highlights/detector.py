from pathlib import Path

from src.config.paths import CACHE_HIGHLIGHTS_DIR
from src.config.settings import HIGHLIGHT_MIN_SCORE
from src.highlights.audio_intensity import (
    get_wav_segment_energies,
    normalize_energy,
)
from src.highlights.highlight_schema import Highlight
from src.highlights.laugh_detector import (
    detect_audio_laugh_by_energy_variation,
    detect_text_laugh,
)
from src.highlights.scorer import score_highlight
from src.utils.file_utils import format_project_path, load_json, save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def detect_highlights(
    transcript_path: str | Path,
    audio_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
) -> Path:
    transcript_path = Path(transcript_path)
    audio_path = Path(audio_path)

    if output_path is None:
        output_path = CACHE_HIGHLIGHTS_DIR / "highlights.json"

    output_path = Path(output_path)

    if output_path.exists() and not force:
        logger.info("Highlights já existem em cache: %s", format_project_path(output_path))
        return output_path

    transcript = load_json(transcript_path)
    segments = [
        segment
        for segment in transcript.get("segments", [])
        if segment.get("text", "").strip()
    ]
    time_ranges = [(segment["start"], segment["end"]) for segment in segments]
    raw_energies = get_wav_segment_energies(audio_path, time_ranges)

    max_energy = max(raw_energies) if raw_energies else 0.0

    highlights = []

    for segment, raw_energy in zip(segments, raw_energies):
        text = segment.get("text", "").strip()

        energy_score = normalize_energy(raw_energy, max_energy)

        text_laugh_score, text_laugh_reasons = detect_text_laugh(text)
        audio_laugh_score, audio_laugh_reasons = detect_audio_laugh_by_energy_variation(
            energy_score,
            text,
        )

        laugh_score = max(text_laugh_score, audio_laugh_score)

        score, reasons = score_highlight(
            text=text,
            energy_score=energy_score,
            laugh_score=laugh_score,
        )

        reasons.extend(text_laugh_reasons)
        reasons.extend(audio_laugh_reasons)

        if score >= HIGHLIGHT_MIN_SCORE:
            highlight = Highlight(
                start=segment["start"],
                end=segment["end"],
                text=text,
                score=score,
                reasons=reasons,
            )

            highlights.append(highlight.model_dump())

    highlights = sorted(highlights, key=lambda item: item["score"], reverse=True)

    save_json(highlights, output_path)

    logger.info("Highlights gerados: %s", len(highlights))
    logger.info("Arquivo salvo em: %s", format_project_path(output_path))

    return output_path
