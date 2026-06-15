from pathlib import Path

from src.editing import shorts_builder
from src.editing.shorts_builder import render_short, render_shorts_from_edit_plan
from src.utils.file_utils import save_json


def test_render_short_builds_expected_ffmpeg_command(
    monkeypatch,
    tmp_path: Path,
) -> None:
    calls = []
    output_dir = tmp_path / "output" / "shorts"

    def fake_run_command(command: list[str]) -> None:
        calls.append(command)
        Path(command[-1]).write_bytes(b"short")

    monkeypatch.setattr(shorts_builder, "run_command", fake_run_command)

    output_path = render_short(
        source_video="input/live_bruta.mp4",
        short={
            "id": "short_01",
            "start": 118.4,
            "duration": 15.0,
        },
        output_dir=output_dir,
    )

    assert output_path == output_dir / "short_01.mp4"
    assert output_path.read_bytes() == b"short"
    assert calls == [
        [
            "ffmpeg",
            "-y",
            "-ss",
            "118.4",
            "-i",
            "input/live_bruta.mp4",
            "-t",
            "15.0",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    ]


def test_render_shorts_from_edit_plan_uses_cache_without_force(
    monkeypatch,
    tmp_path: Path,
) -> None:
    calls = []
    output_dir = tmp_path / "output" / "shorts"
    existing_short = output_dir / "short_01.mp4"
    existing_short.parent.mkdir(parents=True, exist_ok=True)
    existing_short.write_bytes(b"cached")
    edit_plan_path = tmp_path / "cache" / "edit_plans" / "edit_plan.json"

    save_json(
        {
            "source_video": "input/live_bruta.mp4",
            "shorts": [
                {
                    "id": "short_01",
                    "start": 0.0,
                    "duration": 15.0,
                }
            ],
            "long_videos": [],
        },
        edit_plan_path,
    )

    monkeypatch.setattr(shorts_builder, "OUTPUT_SHORTS_DIR", output_dir)
    monkeypatch.setattr(shorts_builder, "run_command", lambda command: calls.append(command))

    rendered = render_shorts_from_edit_plan(edit_plan_path)

    assert rendered == [existing_short]
    assert existing_short.read_bytes() == b"cached"
    assert calls == []
