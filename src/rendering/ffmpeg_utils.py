import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from src.config.paths import CACHE_DIR, OUTPUT_DIR, ROOT_DIR


class FFmpegError(RuntimeError):
    pass


def ensure_tool_available(tool_name: str) -> None:
    if shutil.which(tool_name) is None:
        raise FFmpegError(f"{tool_name} não encontrado no sistema")


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def ensure_safe_project_output_path(output_path: str | Path) -> None:
    path = Path(output_path)

    if not _is_relative_to(path, ROOT_DIR):
        return

    if _is_relative_to(path, CACHE_DIR) or _is_relative_to(path, OUTPUT_DIR):
        return

    raise ValueError(
        "Arquivos gerados dentro do projeto devem ser salvos em cache/ ou output/: "
        f"{path}"
    )


def run_ffmpeg_command(command: list[str], *, error_label: str) -> None:
    ensure_tool_available(command[0])

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        details = (error.stderr or error.stdout or "").strip()
        message = f"Falha ao executar {error_label}"
        if details:
            message = f"{message}: {details}"
        raise FFmpegError(message) from error


def run_ffprobe_json(video_path: str | Path) -> dict[str, Any]:
    ensure_tool_available("ffprobe")

    command = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(video_path),
    ]

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise FFmpegError(f"Falha ao obter metadados de: {video_path}") from error

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise FFmpegError(f"Resposta inválida do ffprobe para: {video_path}") from error
