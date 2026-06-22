from src.subtitles.subtitle_segmenter import (
    filter_segments_by_range,
    get_segments_for_range,
    shift_segments_to_zero,
    split_long_segments,
)
from src.transcription.subtitle_cleaner import SubtitleSegment
from src.transcription.transcript_schema import TranscriptSegment


def test_filter_segments_by_range_uses_overlap_rule() -> None:
    segments = [
        TranscriptSegment(start=8.0, end=10.0, text="fora antes"),
        TranscriptSegment(start=9.5, end=11.0, text="cruza inicio"),
        TranscriptSegment(start=12.0, end=13.0, text="dentro"),
        TranscriptSegment(start=15.0, end=16.0, text="fora depois"),
    ]

    filtered = filter_segments_by_range(segments, start=10.0, end=15.0)

    assert [segment.text for segment in filtered] == ["cruza inicio", "dentro"]


def test_shift_segments_to_zero_clips_to_short_duration() -> None:
    segments = [
        TranscriptSegment(start=9.5, end=11.0, text="cruza inicio"),
        TranscriptSegment(start=14.0, end=16.0, text="cruza fim"),
    ]

    shifted = shift_segments_to_zero(segments, start=10.0, end=15.0)

    assert shifted[0] == SubtitleSegment(start=0.0, end=1.0, text="Cruza inicio")
    assert shifted[1] == SubtitleSegment(start=4.0, end=5.0, text="Cruza fim")


def test_split_long_segments_uses_word_groups_and_proportional_time() -> None:
    segments = [
        SubtitleSegment(
            start=0.0,
            end=8.0,
            text="mano eu não acredito que isso aconteceu agora",
        )
    ]

    split = split_long_segments(segments)

    assert [segment.text for segment in split] == [
        "mano eu",
        "não acredito",
        "que isso",
        "aconteceu agora",
    ]
    assert split[0].start == 0.0
    assert round(split[0].end, 2) == 2.0
    assert round(split[1].start, 2) == 2.0
    assert split[-1].end == 8.0


def test_get_segments_for_range_filters_shifts_and_splits() -> None:
    segments = [
        TranscriptSegment(start=731.3, end=733.5, text="mano olha isso agora mesmo"),
    ]

    subtitle_segments = get_segments_for_range(segments, start=730.0, end=735.0)

    assert subtitle_segments[0].start == 1.3
    assert subtitle_segments[0].end == 3.5
    assert subtitle_segments[0].text == "Mano olha isso agora mesmo"
