import pytest
from pydantic import ValidationError

from src.transcription.transcript_schema import Transcript, TranscriptSegment


def test_transcript_schema_accepts_expected_structure() -> None:
    transcript = Transcript.model_validate(
        {
            "source_audio": "cache/audio/live_bruta.wav",
            "language": "pt",
            "duration": 1.0,
            "segments": [
                {
                    "start": 0.0,
                    "end": 1.0,
                    "text": " texto transcrito ",
                }
            ],
            "metadata": {
                "execution_time_seconds": 1.0,
                "audio_duration_seconds": 1.0,
                "realtime_speed": 1.0,
                "segment_count": 1,
                "model": "tiny",
                "device": "cpu",
                "compute_type": "int8",
                "beam_size": 1,
                "best_of": 1,
                "vad_filter": True,
                "word_timestamps": False,
                "profile": "fast",
            },
        }
    )

    assert transcript.source_audio == "cache/audio/live_bruta.wav"
    assert transcript.language == "pt"
    assert transcript.duration == 1.0
    assert transcript.segments[0].text == "texto transcrito"
    assert transcript.metadata.profile == "fast"


def test_transcript_segment_rejects_end_before_start() -> None:
    with pytest.raises(ValidationError):
        TranscriptSegment(start=2.0, end=1.0, text="texto")


def test_transcript_segment_rejects_empty_text() -> None:
    with pytest.raises(ValidationError):
        TranscriptSegment(start=0.0, end=1.0, text="   ")
