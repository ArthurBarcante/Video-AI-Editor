from pathlib import Path

import pytest

from src.audio import chunker
from src.audio.chunker import build_audio_chunk_ranges, create_audio_chunks
from src.utils.file_utils import load_json


def test_build_audio_chunk_ranges_adds_overlap() -> None:
    chunks = build_audio_chunk_ranges(
        audio_duration=20,
        chunk_duration=10,
        overlap=2,
    )

    assert chunks == [
        {"index": 1, "start": 0.0, "end": 10.0, "duration": 10.0},
        {"index": 2, "start": 8.0, "end": 18.0, "duration": 10.0},
        {"index": 3, "start": 16.0, "end": 20, "duration": 4.0},
    ]


def test_build_audio_chunk_ranges_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError, match="overlap deve ser menor"):
        build_audio_chunk_ranges(
            audio_duration=20,
            chunk_duration=10,
            overlap=10,
        )


def test_create_audio_chunks_writes_metadata(
    monkeypatch: pytest.MonkeyPatch,
    sample_audio: Path,
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "cache" / "audio" / "chunks"

    monkeypatch.setattr(
        chunker,
        "get_video_metadata",
        lambda audio_path: {"duration": 3.0},
    )

    metadata = create_audio_chunks(
        audio_path=sample_audio,
        output_dir=output_dir,
        chunk_duration=2,
        overlap=0,
    )

    assert metadata["chunk_count"] == 2
    assert metadata["chunks_reused_from_cache"] == 0
    assert Path(metadata["metadata_path"]).exists()
    assert load_json(metadata["metadata_path"])["chunk_count"] == 2
    assert Path(metadata["chunks"][0]["path"]).exists()

    cached_metadata = create_audio_chunks(
        audio_path=sample_audio,
        output_dir=output_dir,
        chunk_duration=2,
        overlap=0,
    )

    assert cached_metadata["chunks_reused_from_cache"] == 2
