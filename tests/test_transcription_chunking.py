import pytest

from src.transcription.chunk_merger import merge_chunk_segments
from src.transcription.chunking import build_chunk_ranges


def test_build_chunk_ranges_adds_overlap() -> None:
    chunks = build_chunk_ranges(
        audio_duration=20,
        chunk_duration=10,
        overlap=2,
    )

    assert chunks == [
        {"index": 1, "start": 0.0, "end": 10.0, "duration": 10.0},
        {"index": 2, "start": 8.0, "end": 18.0, "duration": 10.0},
        {"index": 3, "start": 16.0, "end": 20, "duration": 4.0},
    ]


def test_build_chunk_ranges_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError, match="overlap deve ser menor"):
        build_chunk_ranges(
            audio_duration=20,
            chunk_duration=10,
            overlap=10,
        )


def test_merge_chunk_segments_removes_overlap_duplicates() -> None:
    merged = merge_chunk_segments(
        [
            {
                "segments": [
                    {"start": 0.0, "end": 5.0, "text": "fala boa"},
                    {"start": 8.0, "end": 10.0, "text": "repete"},
                ]
            },
            {
                "segments": [
                    {"start": 10.5, "end": 12.0, "text": "repete"},
                    {"start": 12.5, "end": 14.0, "text": "nova fala"},
                ]
            },
        ]
    )

    assert merged == [
        {"start": 0.0, "end": 5.0, "text": "fala boa"},
        {"start": 8.0, "end": 10.0, "text": "repete"},
        {"start": 12.5, "end": 14.0, "text": "nova fala"},
    ]
