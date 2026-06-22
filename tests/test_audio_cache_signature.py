from pathlib import Path

from src.audio.cache_signature import build_video_cache_signature


def test_build_video_cache_signature_changes_when_file_changes(tmp_path: Path) -> None:
    video_path = tmp_path / "live.mp4"
    video_path.write_bytes(b"first")

    first_signature = build_video_cache_signature(video_path)

    video_path.write_bytes(b"second version")

    assert build_video_cache_signature(video_path) != first_signature
