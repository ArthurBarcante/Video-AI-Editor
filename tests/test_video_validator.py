from pathlib import Path

import pytest

from src.video.validator import validate_video_file


def test_validate_video_file_accepts_valid_mp4(sample_video: Path) -> None:
    assert validate_video_file(sample_video) == sample_video


def test_validate_video_file_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Vídeo não encontrado"):
        validate_video_file(tmp_path / "missing.mp4")


def test_validate_video_file_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="O caminho não é um arquivo"):
        validate_video_file(tmp_path)


def test_validate_video_file_rejects_non_mp4(tmp_path: Path) -> None:
    video_path = tmp_path / "sample.mov"
    video_path.write_bytes(b"fake")

    with pytest.raises(ValueError, match="O arquivo não é .mp4"):
        validate_video_file(video_path)


def test_validate_video_file_rejects_empty_mp4(tmp_path: Path) -> None:
    video_path = tmp_path / "empty.mp4"
    video_path.touch()

    with pytest.raises(ValueError, match="O arquivo está vazio"):
        validate_video_file(video_path)


def test_validate_video_file_rejects_video_without_audio(
    video_without_audio: Path,
) -> None:
    with pytest.raises(ValueError, match="não possui stream de áudio"):
        validate_video_file(video_without_audio)
