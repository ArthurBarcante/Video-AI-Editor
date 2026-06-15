from pathlib import Path

from src.editing import long_video_builder
from src.editing.long_video_builder import (
    concat_segments,
    render_long_video,
    render_long_videos_from_edit_plan,
)
from src.utils.file_utils import save_json


def test_render_long_video_cuts_segments_and_concats(
    monkeypatch,
    tmp_path: Path,
) -> None:
    calls = []
    output_dir = tmp_path / "output" / "long"

    def fake_run_command(command: list[str]) -> None:
        calls.append(command)
        Path(command[-1]).write_bytes(b"video")

    monkeypatch.setattr(long_video_builder, "run_command", fake_run_command)

    output_path = render_long_video(
        source_video="input/live_bruta.mp4",
        long_video={
            "id": "video_01",
            "segments": [
                {"start": 10.0, "duration": 12.0},
                {"start": 30.0, "duration": 15.0},
            ],
        },
        output_dir=output_dir,
    )

    assert output_path == output_dir / "video_01.mp4"
    assert output_path.read_bytes() == b"video"
    assert calls[0][:8] == [
        "ffmpeg",
        "-y",
        "-ss",
        "10.0",
        "-i",
        "input/live_bruta.mp4",
        "-t",
        "12.0",
    ]
    assert calls[1][:8] == [
        "ffmpeg",
        "-y",
        "-ss",
        "30.0",
        "-i",
        "input/live_bruta.mp4",
        "-t",
        "15.0",
    ]
    assert calls[2][:7] == ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i"]


def test_concat_segments_removes_concat_file(
    monkeypatch,
    tmp_path: Path,
) -> None:
    segment_path = tmp_path / "segment_001.mp4"
    output_path = tmp_path / "output" / "video_01.mp4"
    segment_path.write_bytes(b"segment")

    def fake_run_command(command: list[str]) -> None:
        Path(command[-1]).write_bytes(b"long")

    monkeypatch.setattr(long_video_builder, "run_command", fake_run_command)

    concat_segments([segment_path], output_path)

    assert output_path.read_bytes() == b"long"
    assert not (output_path.parent / "video_01_concat.txt").exists()


def test_render_long_videos_from_edit_plan_uses_cache_without_force(
    monkeypatch,
    tmp_path: Path,
) -> None:
    calls = []
    output_dir = tmp_path / "output" / "long"
    existing_video = output_dir / "video_01.mp4"
    existing_video.parent.mkdir(parents=True, exist_ok=True)
    existing_video.write_bytes(b"cached")
    edit_plan_path = tmp_path / "cache" / "edit_plans" / "edit_plan.json"

    save_json(
        {
            "source_video": "input/live_bruta.mp4",
            "shorts": [],
            "long_videos": [
                {
                    "id": "video_01",
                    "segments": [{"start": 0.0, "duration": 15.0}],
                }
            ],
        },
        edit_plan_path,
    )

    monkeypatch.setattr(long_video_builder, "OUTPUT_LONG_DIR", output_dir)
    monkeypatch.setattr(long_video_builder, "run_command", lambda command: calls.append(command))

    rendered = render_long_videos_from_edit_plan(edit_plan_path)

    assert rendered == [existing_video]
    assert existing_video.read_bytes() == b"cached"
    assert calls == []
