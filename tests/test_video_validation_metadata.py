from pathlib import Path

from src.video.validation_metadata import (
    build_validation_metadata,
    save_validation_metadata,
)
from src.utils.file_utils import load_json


def test_build_validation_metadata_uses_expected_fields() -> None:
    metadata = build_validation_metadata(
        video_path="input/live_bruta.mp4",
        metadata={
            "duration": 3441.19,
            "width": 1920,
            "height": 1080,
            "fps": 60,
            "video_codec": "h264",
            "audio_codec": "aac",
            "bitrate": 2500000,
            "size_bytes": 1234567890,
        },
    )

    assert metadata["file_name"] == "live_bruta.mp4"
    assert metadata["source_path"] == "input/live_bruta.mp4"
    assert metadata["duration"] == 3441.19
    assert metadata["width"] == 1920
    assert metadata["height"] == 1080
    assert metadata["fps"] == 60
    assert metadata["codec"] == "h264"
    assert metadata["audio_codec"] == "aac"
    assert metadata["bitrate"] == 2500000
    assert metadata["file_size_bytes"] == 1234567890
    assert metadata["validated_at"]


def test_save_validation_metadata_writes_json(tmp_path: Path) -> None:
    output_path = save_validation_metadata(
        video_path="input/live_bruta.mp4",
        metadata={
            "duration": 3441.19,
            "width": 1920,
            "height": 1080,
            "fps": 60,
            "video_codec": "h264",
            "audio_codec": "aac",
            "bitrate": 2500000,
            "size_bytes": 1234567890,
        },
        output_dir=tmp_path,
    )

    assert output_path == tmp_path / "live_bruta_validation_metadata.json"
    assert load_json(output_path)["file_name"] == "live_bruta.mp4"
