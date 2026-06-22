import time
from pathlib import Path
from typing import Any

from src.config.settings import (
    WHISPER_BEAM_SIZE,
    WHISPER_BEST_OF,
    WHISPER_CONDITION_ON_PREVIOUS_TEXT,
    WHISPER_LANGUAGE,
    WHISPER_PROFILE,
    WHISPER_VAD_FILTER,
    WHISPER_WORD_TIMESTAMPS,
)
from src.transcription.text_cleaner import clean_transcript_text
from src.transcription.transcription_profiles import get_transcription_profile
from src.utils.file_utils import load_json, save_json


def transcribe_chunk(
    model: Any,
    chunk_audio_path: str | Path,
    chunk_start_offset: float,
    output_path: str | Path,
    force: bool = False,
) -> dict:
    output_path = Path(output_path)

    if output_path.exists() and not force:
        data = load_json(output_path)
        data["_reused_from_cache"] = True
        return data

    profile = get_transcription_profile(WHISPER_PROFILE)
    beam_size = WHISPER_BEAM_SIZE or profile["beam_size"]
    best_of = WHISPER_BEST_OF or profile["best_of"]

    started_at = time.perf_counter()

    segments, info = model.transcribe(
        str(chunk_audio_path),
        language=WHISPER_LANGUAGE,
        vad_filter=WHISPER_VAD_FILTER,
        vad_parameters=profile.get("vad_parameters"),
        beam_size=beam_size,
        best_of=best_of,
        temperature=0,
        condition_on_previous_text=WHISPER_CONDITION_ON_PREVIOUS_TEXT,
        word_timestamps=WHISPER_WORD_TIMESTAMPS,
    )

    output_segments = []

    for segment in segments:
        text = clean_transcript_text(segment.text)

        if not text:
            continue

        output_segments.append(
            {
                "start": float(segment.start + chunk_start_offset),
                "end": float(segment.end + chunk_start_offset),
                "text": text,
            }
        )

    elapsed = time.perf_counter() - started_at

    data = {
        "chunk_audio": str(chunk_audio_path),
        "chunk_start_offset": chunk_start_offset,
        "language": getattr(info, "language", WHISPER_LANGUAGE),
        "duration": float(getattr(info, "duration", 0) or 0),
        "segments": output_segments,
        "metadata": {
            "execution_time_seconds": round(elapsed, 2),
            "segment_count": len(output_segments),
        },
    }

    save_json(data, output_path)

    data["_reused_from_cache"] = False
    return data
