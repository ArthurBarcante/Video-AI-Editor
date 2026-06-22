from pathlib import Path

import pytest

from src.audio import extractor
from src.audio.audio_validator import validate_audio_file
from src.audio.cache_signature import build_video_cache_signature
from src.audio.extractor import extract_audio_from_video
from src.config.paths import ROOT_DIR
from src.rendering.ffmpeg_utils import FFmpegError
from src.utils.file_utils import load_json


def test_extract_audio_from_video_creates_non_empty_wav(
    sample_video: Path,
    tmp_path: Path,
) -> None:
    audio_dir = tmp_path / "cache" / "audio"
    signature = build_video_cache_signature(sample_video)

    audio_path = extract_audio_from_video(sample_video, output_dir=audio_dir)

    assert audio_path == audio_dir / f"sample_{signature}.wav"
    assert audio_path.exists()
    assert audio_path.stat().st_size > 0
    assert validate_audio_file(audio_path) == audio_path

    metadata_path = audio_dir / f"sample_{signature}_audio_metadata.json"
    metadata = load_json(metadata_path)
    assert metadata["audio_path"] == str(audio_path)
    assert metadata["cache_signature"] == signature
    assert metadata["signature_strategy"] == "file_size_modified_time"
    assert metadata["source_file_size_bytes"] == sample_video.stat().st_size
    assert metadata["source_modified_time_ns"] == sample_video.stat().st_mtime_ns
    assert metadata["execution_time_seconds"] >= 0
    assert metadata["sample_rate"] == extractor.AUDIO_SAMPLE_RATE
    assert metadata["channels"] == extractor.AUDIO_CHANNELS
    assert metadata["codec"] == extractor.AUDIO_CODEC
    assert metadata["file_size_bytes"] == audio_path.stat().st_size
    assert metadata["fast_test_mode"] is False
    assert metadata["test_duration_seconds"] is None
    assert metadata["chunks_enabled"] is True
    assert metadata["chunk_count"] >= 1
    assert metadata["chunks_metadata_path"]
    assert load_json(metadata["chunks_metadata_path"])["chunk_count"] >= 1


def test_extract_audio_from_video_validates_cached_wav(
    sample_video: Path,
    tmp_path: Path,
) -> None:
    audio_dir = tmp_path / "cache" / "audio"
    audio_path = extract_audio_from_video(sample_video, output_dir=audio_dir)

    cached_path = extract_audio_from_video(sample_video, output_dir=audio_dir)

    assert cached_path == audio_path


def test_extract_audio_from_video_supports_fast_test_mode(
    monkeypatch: pytest.MonkeyPatch,
    sample_video: Path,
    tmp_path: Path,
) -> None:
    audio_dir = tmp_path / "cache" / "audio"
    monkeypatch.setattr(extractor, "AUDIO_FAST_TEST_MODE", True)
    monkeypatch.setattr(extractor, "AUDIO_TEST_DURATION", 1)
    signature = build_video_cache_signature(sample_video)

    audio_path = extract_audio_from_video(sample_video, output_dir=audio_dir)

    metadata = load_json(audio_dir / f"sample_{signature}_audio_metadata.json")
    assert audio_path.exists()
    assert metadata["fast_test_mode"] is True
    assert metadata["test_duration_seconds"] == 1


def test_extract_audio_from_video_fails_clearly_without_audio(
    video_without_audio: Path,
    tmp_path: Path,
) -> None:
    with pytest.raises(FFmpegError, match="Falha ao executar extração de áudio"):
        extract_audio_from_video(video_without_audio, output_dir=tmp_path / "audio")


def test_extract_audio_from_video_rejects_project_root_output(
    sample_video: Path,
) -> None:
    with pytest.raises(ValueError, match="cache/ ou output"):
        extract_audio_from_video(sample_video, output_dir=ROOT_DIR)
