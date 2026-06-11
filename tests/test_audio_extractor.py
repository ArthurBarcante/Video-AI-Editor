from pathlib import Path

import pytest

from src.audio.extractor import extract_audio_from_video
from src.config.paths import ROOT_DIR
from src.rendering.ffmpeg_utils import FFmpegError


def test_extract_audio_from_video_creates_non_empty_wav(
    sample_video: Path,
    tmp_path: Path,
) -> None:
    audio_dir = tmp_path / "cache" / "audio"

    audio_path = extract_audio_from_video(sample_video, output_dir=audio_dir)

    assert audio_path == audio_dir / "sample.wav"
    assert audio_path.exists()
    assert audio_path.stat().st_size > 0


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
