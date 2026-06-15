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


def test_render_short_mixes_sfx_when_asset_exists(
    monkeypatch,
    tmp_path: Path,
) -> None:
    calls = []
    output_dir = tmp_path / "output" / "shorts"
    sfx_path = tmp_path / "assets" / "sfx" / "pop.mp3"
    sfx_path.parent.mkdir(parents=True, exist_ok=True)
    sfx_path.write_bytes(b"sfx")

    def fake_run_command(command: list[str]) -> None:
        calls.append(command)
        Path(command[-1]).write_bytes(b"short")

    monkeypatch.setattr(shorts_builder, "run_command", fake_run_command)
    monkeypatch.setattr(shorts_builder, "resolve_sfx_path", lambda name: sfx_path)

    output_path = render_short(
        source_video="input/live_bruta.mp4",
        short={
            "id": "short_01",
            "start": 118.0,
            "duration": 15.0,
            "actions": [
                {
                    "type": "sfx",
                    "time": 120.5,
                    "name": "pop",
                    "volume": 0.25,
                    "reason": "sfx por palavra-chave",
                }
            ],
        },
        output_dir=output_dir,
    )

    assert output_path == output_dir / "short_01.mp4"
    command = calls[0]
    assert command.count("-i") == 2
    assert str(sfx_path) in command
    assert command.index("-t") > command.index(str(sfx_path))
    assert "-filter_complex" in command
    filter_complex = command[command.index("-filter_complex") + 1]
    assert "[1:a]volume=0.25,adelay=2500|2500[sfx1]" in filter_complex
    assert "[a0][sfx1]amix=inputs=2:duration=first[aout]" in filter_complex
    assert command[command.index("-map") + 1] == "0:v"
    assert "[aout]" in command


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
