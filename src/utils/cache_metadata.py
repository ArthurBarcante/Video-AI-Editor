from pathlib import Path

from src.utils.file_utils import load_json, save_json


def get_cache_metadata_path(output_path: str | Path) -> Path:
    output_path = Path(output_path)
    return output_path.with_name(f"{output_path.stem}.meta.json")


def build_source_signature(path: str | Path) -> dict:
    source_path = Path(path)

    if not source_path.exists():
        return {
            "path": str(source_path),
            "exists": False,
            "size_bytes": None,
            "modified_time_ns": None,
        }

    stat = source_path.stat()

    return {
        "path": str(source_path),
        "exists": True,
        "size_bytes": stat.st_size,
        "modified_time_ns": stat.st_mtime_ns,
    }


def build_cache_metadata(sources: list[str | Path]) -> dict:
    return {
        "sources": [
            build_source_signature(source)
            for source in sources
        ]
    }


def is_cache_valid(output_path: str | Path, sources: list[str | Path]) -> bool:
    output_path = Path(output_path)
    metadata_path = get_cache_metadata_path(output_path)

    if not output_path.exists() or not metadata_path.exists():
        return False

    return load_json(metadata_path) == build_cache_metadata(sources)


def save_cache_metadata(output_path: str | Path, sources: list[str | Path]) -> Path:
    metadata_path = get_cache_metadata_path(output_path)
    save_json(build_cache_metadata(sources), metadata_path)
    return metadata_path
