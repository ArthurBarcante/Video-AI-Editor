from pathlib import Path

from src.config.paths import CACHE_EMOTIONS_DIR
from src.emotion.emotion_rules import detect_emotion_from_text
from src.emotion.emotion_schema import EmotionAnalysis, EmotionSegment
from src.highlights.audio_intensity import (
    get_audio_energy,
    normalize_energy,
    read_wav_mono,
)
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.utils.file_utils import format_project_path, load_json, save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def analyze_emotions(
    transcript_path: str | Path,
    audio_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
) -> Path:
    transcript_path = Path(transcript_path)
    audio_path = Path(audio_path)

    if output_path is None:
        output_path = CACHE_EMOTIONS_DIR / "emotions.json"

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        logger.info("Emoções já existem em cache: %s", format_project_path(output_path))
        return output_path

    transcript = load_json(transcript_path)
    segments = [
        segment
        for segment in transcript.get("segments", [])
        if segment.get("text", "").strip()
    ]
    audio, sample_rate = read_wav_mono(audio_path)

    raw_energies = [
        get_audio_energy(
            audio=audio,
            sample_rate=sample_rate,
            start=segment["start"],
            end=segment["end"],
        )
        for segment in segments
    ]

    max_energy = max(raw_energies) if raw_energies else 0.0
    emotion_segments = []

    for segment, raw_energy in zip(segments, raw_energies):
        text = segment.get("text", "").strip()
        audio_intensity = normalize_energy(raw_energy, max_energy)

        emotion, text_score, reasons = detect_emotion_from_text(text)
        emotion_score = text_score

        if audio_intensity >= 0.70 and emotion != "neutral":
            emotion_score += 0.20
            reasons.append("alta intensidade de áudio")
        elif audio_intensity >= 0.45 and emotion != "neutral":
            emotion_score += 0.10
            reasons.append("intensidade média de áudio")

        emotion_segment = EmotionSegment(
            start=segment["start"],
            end=segment["end"],
            text=text,
            emotion=emotion,
            emotion_score=round(min(emotion_score, 1.0), 4),
            audio_intensity=round(audio_intensity, 4),
            reasons=reasons,
        )

        emotion_segments.append(emotion_segment)

    analysis = EmotionAnalysis(
        source_transcript=format_project_path(transcript_path),
        source_audio=format_project_path(audio_path),
        segments=emotion_segments,
    )

    save_json(analysis.model_dump(), output_path)

    logger.info("Análise emocional salva em: %s", format_project_path(output_path))

    return output_path
