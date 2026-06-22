from datetime import datetime
from pathlib import Path

from src.config.paths import CACHE_METADATA_DIR
from src.utils.file_utils import format_project_path, save_json


def build_validation_metadata(video_path: str | Path, metadata: dict) -> dict:
    path = Path(video_path)

    return {
        "file_name": path.name,
        "source_path": format_project_path(path),
        "duration": metadata["duration"],
        "width": metadata["width"],
        "height": metadata["height"],
        "fps": metadata["fps"],
        "codec": metadata["video_codec"],
        "audio_codec": metadata["audio_codec"],
        "bitrate": metadata["bitrate"],
        "file_size_bytes": metadata["size_bytes"],
        "validated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }


def save_validation_metadata(
    video_path: str | Path,
    metadata: dict,
    output_dir: str | Path = CACHE_METADATA_DIR,
) -> Path:
    path = Path(video_path)
    output_dir = Path(output_dir)
    output_path = output_dir / f"{path.stem}_validation_metadata.json"

    save_json(
        build_validation_metadata(
            video_path=path,
            metadata=metadata,
        ),
        output_path,
    )

    return output_path
