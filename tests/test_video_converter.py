from pathlib import Path

import pytest

from src.config.paths import ROOT_DIR
from src.rendering.ffmpeg_utils import FFmpegError
from src.video.converter import (
    convert_fps,
    convert_to_mp4,
    cut_video_segment,
    resize_video,
)
from src.video.metadata import get_video_metadata
from src.video.validator import validate_video_file


def assert_valid_non_empty_mp4(video_path: Path) -> None:
    assert video_path.suffix == ".mp4"
    assert video_path.exists()
    assert video_path.stat().st_size > 0
    validate_video_file(video_path)


def test_convert_to_mp4_creates_valid_output(
    sample_video: Path,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "cache" / "video" / "converted.mp4"

    converted = convert_to_mp4(sample_video, output_path)

    assert converted == output_path
    assert_valid_non_empty_mp4(converted)


def test_resize_video_changes_resolution(sample_video: Path, tmp_path: Path) -> None:
    output_path = tmp_path / "cache" / "video" / "resized.mp4"

    resized = resize_video(sample_video, output_path, width=80, height=60)
    metadata = get_video_metadata(resized)

    assert_valid_non_empty_mp4(resized)
    assert metadata["width"] == 80
    assert metadata["height"] == 60


def test_convert_fps_changes_frame_rate(sample_video: Path, tmp_path: Path) -> None:
    output_path = tmp_path / "cache" / "video" / "fps_15.mp4"

    converted = convert_fps(sample_video, output_path, fps=15)
    metadata = get_video_metadata(converted)

    assert_valid_non_empty_mp4(converted)
    assert metadata["fps"] == 15.0


def test_cut_video_segment_creates_short_valid_clip(
    sample_video: Path,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "cache" / "video" / "sample_10s.mp4"

    clip = cut_video_segment(
        sample_video,
        output_path,
        start="00:00:00",
        end="00:00:00.50",
    )

    assert_valid_non_empty_mp4(clip)
    assert get_video_metadata(clip)["duration"] <= 1.0


def test_converter_fails_clearly_for_invalid_input(tmp_path: Path) -> None:
    invalid_video = tmp_path / "invalid.mp4"
    invalid_video.write_text("not a real mp4")

    with pytest.raises(FFmpegError, match="Falha ao executar conversão para MP4"):
        convert_to_mp4(invalid_video, tmp_path / "cache" / "video" / "out.mp4")


def test_converter_rejects_project_root_output(sample_video: Path) -> None:
    with pytest.raises(ValueError, match="cache/ ou output"):
        convert_to_mp4(sample_video, ROOT_DIR / "converted.mp4")
