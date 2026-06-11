import json
from pathlib import Path
from typing import Any

from src.config.paths import ROOT_DIR


def ensure_dir(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data: Any, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def format_project_path(path: str | Path) -> str:
    resolved_path = Path(path)

    try:
        return str(resolved_path.relative_to(ROOT_DIR))
    except ValueError:
        return str(resolved_path)
