from src.transcription.subtitle_cleaner import (
    clean_subtitle_text,
    prepare_subtitle_segments,
)
from src.transcription.transcript_schema import TranscriptSegment


def test_clean_subtitle_text_removes_hesitation_and_repetition() -> None:
    assert clean_subtitle_text("é... é... então") == "Então"
    assert clean_subtitle_text("mano mano mano") == "Mano"
    assert clean_subtitle_text("ahhhhh") == "Ah"


def test_prepare_subtitle_segments_splits_long_segments() -> None:
    segments = [
        TranscriptSegment(
            start=0.0,
            end=12.0,
            text="eu estava andando na rua quando encontrei um cara diferente",
        )
    ]

    prepared = prepare_subtitle_segments(segments)

    assert len(prepared) == 2
    assert prepared[0].start == 0.0
    assert prepared[0].end == 6.0
    assert prepared[1].start == 6.0
    assert prepared[1].end == 12.0


def test_prepare_subtitle_segments_applies_minimum_duration() -> None:
    segments = [
        TranscriptSegment(start=3.0, end=3.4, text="fala curta"),
    ]

    prepared = prepare_subtitle_segments(segments)

    assert prepared[0].start == 3.0
    assert prepared[0].end == 4.0
