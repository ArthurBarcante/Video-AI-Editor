from pathlib import Path

from src.rendering import verticalizer
from src.rendering.verticalizer import (
    build_vertical_filter,
    verticalize_all_shorts,
    verticalize_with_blur,
)


def test_build_vertical_filter_without_blur() -> None:
    assert build_vertical_filter(540, 960, blur_enabled=False) == (
        "scale=540:960:force_original_aspect_ratio=decrease,"
        "pad=540:960:(ow-iw)/2:(oh-ih)/2"
    )


def test_verticalize_with_blur_builds_expected_ffmpeg_command(
    monkeypatch,
    tmp_path: Path,
) -> None:
    calls = []
    input_path = tmp_path / "output" / "shorts" / "short_01.mp4"
    output_path = tmp_path / "output" / "vertical" / "short_01_vertical.mp4"
    input_path.parent.mkdir(parents=True, exist_ok=True)
    input_path.write_bytes(b"short")

    def fake_run_command(command: list[str]) -> None:
        calls.append(command)
        Path(command[-1]).write_bytes(b"vertical")

    monkeypatch.setattr(verticalizer, "run_command", fake_run_command)

    result = verticalize_with_blur(
        input_path=input_path,
        output_path=output_path,
    )

    assert result == output_path
    assert output_path.read_bytes() == b"vertical"
    command = calls[0]
    assert command[:4] == ["ffmpeg", "-y", "-i", str(input_path)]
    assert "-filter_complex" in command
    filter_complex = command[command.index("-filter_complex") + 1]
    assert "scale=1080:1920:force_original_aspect_ratio=increase" in filter_complex
    assert "crop=1080:1920,boxblur=20:1[bg]" in filter_complex
    assert "force_original_aspect_ratio=decrease" in filter_complex
    assert "[bg][fg]overlay=(W-w)/2:(H-h)/2" in filter_complex
    assert "-preset" in command
    assert "veryfast" in command
    assert "-crf" in command
    assert "28" in command
    assert command[command.index("-c:a") + 1] == "copy"


def test_verticalize_with_blur_supports_fast_mode_and_no_blur(
    monkeypatch,
    tmp_path: Path,
) -> None:
    calls = []
    input_path = tmp_path / "output" / "shorts" / "short_01.mp4"
    output_path = tmp_path / "output" / "vertical" / "short_01_vertical.mp4"
    input_path.parent.mkdir(parents=True, exist_ok=True)
    input_path.write_bytes(b"short")

    def fake_run_command(command: list[str]) -> None:
        calls.append(command)
        Path(command[-1]).write_bytes(b"vertical")

    monkeypatch.setattr(verticalizer, "run_command", fake_run_command)
    monkeypatch.setattr(verticalizer, "VERTICAL_FAST_MODE", True)
    monkeypatch.setattr(verticalizer, "VERTICAL_BLUR_ENABLED", False)

    verticalize_with_blur(
        input_path=input_path,
        output_path=output_path,
    )

    command = calls[0]
    assert "-vf" in command
    assert "-filter_complex" not in command
    video_filter = command[command.index("-vf") + 1]
    assert "scale=540:960:force_original_aspect_ratio=decrease" in video_filter
    assert "pad=540:960:(ow-iw)/2:(oh-ih)/2" in video_filter


def test_verticalize_all_shorts_processes_mp4_files(
    monkeypatch,
    tmp_path: Path,
) -> None:
    shorts_dir = tmp_path / "output" / "shorts"
    output_dir = tmp_path / "output" / "vertical"
    shorts_dir.mkdir(parents=True)
    (shorts_dir / "short_02.mp4").write_bytes(b"short")
    (shorts_dir / "short_01.mp4").write_bytes(b"short")
    (shorts_dir / "notes.txt").write_text("ignore", encoding="utf-8")
    calls = []

    def fake_verticalize_with_blur(
        input_path: str | Path,
        output_path: str | Path | None = None,
        force: bool = False,
    ) -> Path:
        calls.append((Path(input_path).name, Path(output_path).name, force))
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(b"vertical")
        return Path(output_path)

    monkeypatch.setattr(verticalizer, "VERTICAL_RENDER_PARALLEL", False)
    monkeypatch.setattr(
        verticalizer,
        "verticalize_with_blur",
        fake_verticalize_with_blur,
    )

    rendered = verticalize_all_shorts(
        shorts_dir=shorts_dir,
        output_dir=output_dir,
        force=True,
    )

    assert rendered == [
        output_dir / "short_01_vertical.mp4",
        output_dir / "short_02_vertical.mp4",
    ]
    assert calls == [
        ("short_01.mp4", "short_01_vertical.mp4", True),
        ("short_02.mp4", "short_02_vertical.mp4", True),
    ]
