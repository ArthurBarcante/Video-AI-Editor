from pathlib import Path

from src.config.paths import INPUT_DIR


SUPPORTED_VIDEO_EXTENSIONS = {".mp4"}


def list_input_videos(input_dir: Path = INPUT_DIR) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Pasta de input não encontrada: {input_dir}")

    videos = [
        file
        for file in input_dir.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS
    ]

    return sorted(videos)


def get_first_input_video(input_dir: Path = INPUT_DIR) -> Path:
    videos = list_input_videos(input_dir)

    if not videos:
        raise FileNotFoundError(
            f"Nenhum arquivo .mp4 encontrado na pasta: {input_dir}"
        )

    return videos[0]