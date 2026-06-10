import json
from pathlib import Path
from typing import Any


def cache_exists(path: str | Path) -> bool:
    return Path(path).exists()


def load_cache(path: str | Path) -> Any:
    cache_path = Path(path)

    if not cache_path.exists():
        raise FileNotFoundError(f"Cache não encontrado: {cache_path}")

    with cache_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(data: Any, path: str | Path) -> Path:
    cache_path = Path(path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    with cache_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return cache_path


def should_use_cache(path: str | Path, force: bool = False) -> bool:
    if force:
        return False

    return cache_exists(path)
