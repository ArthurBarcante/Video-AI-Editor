from pathlib import Path

from src.rendering import verticalizer
from src.rendering.verticalizer import verticalize_all_shorts, verticalize_with_blur


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
    assert "scale=540:960:force_original_aspect_ratio=increase" in filter_complex
    assert "crop=540:960,boxblur=12:1,scale=1080:1920[bg]" in filter_complex
    assert "force_original_aspect_ratio=decrease" in filter_complex
    assert "[bg][fg]overlay=(W-w)/2:(H-h)/2" in filter_complex
    assert "-preset" in command
    assert "veryfast" in command


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
        width: int = 1080,
        height: int = 1920,
        force: bool = False,
    ) -> Path:
        calls.append((Path(input_path).name, Path(output_path).name, width, height, force))
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(b"vertical")
        return Path(output_path)

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
        ("short_01.mp4", "short_01_vertical.mp4", 1080, 1920, True),
        ("short_02.mp4", "short_02_vertical.mp4", 1080, 1920, True),
    ]
