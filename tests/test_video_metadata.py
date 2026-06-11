from pathlib import Path

import pytest

from src.rendering.ffmpeg_utils import FFmpegError
from src.video.metadata import get_video_metadata, get_video_streams


def test_get_video_streams_includes_audio_and_video(sample_video: Path) -> None:
    streams = get_video_streams(sample_video)["streams"]

    assert any(stream["codec_type"] == "video" for stream in streams)
    assert any(stream["codec_type"] == "audio" for stream in streams)


def test_get_video_metadata_returns_required_fields(sample_video: Path) -> None:
    metadata = get_video_metadata(sample_video)

    assert metadata["duration"] > 0
    assert metadata["size_bytes"] > 0
    assert metadata["video_codec"] == "h264"
    assert metadata["audio_codec"] == "aac"
    assert metadata["width"] == 160
    assert metadata["height"] == 120
    assert metadata["fps"] == 25.0


def test_get_video_metadata_fails_clearly_for_invalid_file(tmp_path: Path) -> None:
    invalid_video = tmp_path / "invalid.mp4"
    invalid_video.write_text("not a real mp4")

    with pytest.raises(FFmpegError, match="Falha ao obter metadados"):
        get_video_metadata(invalid_video)
