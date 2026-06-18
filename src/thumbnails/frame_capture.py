import subprocess
from pathlib import Path

from src.rendering.ffmpeg_utils import ensure_safe_project_output_path, run_command


def _build_capture_command(
    video_path: str | Path,
    timestamp: float,
    output_path: str | Path,
) -> list[str]:
    return [
        "ffmpeg",
        "-y",
        "-ss",
        str(timestamp),
        "-i",
        str(video_path),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output_path),
    ]


def capture_frame(
    video_path: str | Path,
    timestamp: float,
    output_path: str | Path,
) -> Path:
    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = _build_capture_command(
        video_path=video_path,
        timestamp=timestamp,
        output_path=output_path,
    )

    try:
        run_command(command)
    except subprocess.CalledProcessError:
        if timestamp <= 0:
            raise

        run_command(
            _build_capture_command(
                video_path=video_path,
                timestamp=0,
                output_path=output_path,
            )
        )

    if (not output_path.exists() or output_path.stat().st_size == 0) and timestamp > 0:
        run_command(
            _build_capture_command(
                video_path=video_path,
                timestamp=0,
                output_path=output_path,
            )
        )

    return output_path
