from pathlib import Path

import pytest

from src.video.reader import get_first_input_video, list_input_videos


def test_list_input_videos_finds_only_mp4_files(tmp_path: Path) -> None:
    first = tmp_path / "a.mp4"
    second = tmp_path / "b.MP4"
    ignored = tmp_path / "clip.mov"

    first.write_bytes(b"mp4")
    second.write_bytes(b"mp4")
    ignored.write_bytes(b"mov")

    assert list_input_videos(tmp_path) == [first, second]
    assert get_first_input_video(tmp_path) == first


def test_get_first_input_video_fails_clearly_without_mp4(tmp_path: Path) -> None:
    (tmp_path / "readme.txt").write_text("sem video")

    with pytest.raises(FileNotFoundError, match="Nenhum arquivo .mp4 encontrado"):
        get_first_input_video(tmp_path)


def test_list_input_videos_fails_clearly_when_input_dir_is_missing(
    tmp_path: Path,
) -> None:
    missing_dir = tmp_path / "input"

    with pytest.raises(FileNotFoundError, match="Pasta de input não encontrada"):
        list_input_videos(missing_dir)
