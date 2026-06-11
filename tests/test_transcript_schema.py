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
        }
    )

    assert transcript.source_audio == "cache/audio/live_bruta.wav"
    assert transcript.language == "pt"
    assert transcript.duration == 1.0
    assert transcript.segments[0].text == "texto transcrito"


def test_transcript_segment_rejects_end_before_start() -> None:
    with pytest.raises(ValidationError):
        TranscriptSegment(start=2.0, end=1.0, text="texto")


def test_transcript_segment_rejects_empty_text() -> None:
    with pytest.raises(ValidationError):
        TranscriptSegment(start=0.0, end=1.0, text="   ")
