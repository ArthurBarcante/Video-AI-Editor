import shutil
import subprocess
from pathlib import Path

import pytest


def require_ffmpeg_tools() -> None:
    missing = [tool for tool in ("ffmpeg", "ffprobe") if shutil.which(tool) is None]
    if missing:
        pytest.skip(f"Ferramenta(s) não instalada(s): {', '.join(missing)}")


def make_test_video(
    output_path: Path,
    *,
    duration: float = 1.0,
    with_audio: bool = True,
) -> Path:
    require_ffmpeg_tools()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "testsrc=size=160x120:rate=25",
    ]

    if with_audio:
        command.extend(
            [
                "-f",
                "lavfi",
                "-i",
                "sine=frequency=1000:sample_rate=44100",
            ]
        )

    command.extend(
        [
            "-t",
            str(duration),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
        ]
    )

    if with_audio:
        command.extend(["-c:a", "aac", "-shortest"])

    command.append(str(output_path))

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        pytest.fail(f"Falha ao gerar vídeo de teste com FFmpeg: {result.stderr}")

    return output_path


def make_test_audio(output_path: Path, *, duration: float = 0.5) -> Path:
    require_ffmpeg_tools()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "sine=frequency=1000:sample_rate=16000",
        "-t",
        str(duration),
        "-acodec",
        "pcm_s16le",
        "-ac",
        "1",
        str(output_path),
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        pytest.fail(f"Falha ao gerar áudio de teste com FFmpeg: {result.stderr}")

    return output_path


@pytest.fixture
def sample_video(tmp_path: Path) -> Path:
    return make_test_video(tmp_path / "sample.mp4")


@pytest.fixture
def video_without_audio(tmp_path: Path) -> Path:
    return make_test_video(tmp_path / "no_audio.mp4", with_audio=False)


@pytest.fixture
def sample_audio(tmp_path: Path) -> Path:
    return make_test_audio(tmp_path / "sample.wav")
