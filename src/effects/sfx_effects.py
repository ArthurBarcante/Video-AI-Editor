from pathlib import Path

from src.config.paths import ASSETS_SFX_DIR


SFX_LIBRARY = {
    "pop": ASSETS_SFX_DIR / "pop.mp3",
    "impact": ASSETS_SFX_DIR / "impact.mp3",
    "laugh": ASSETS_SFX_DIR / "laugh.mp3",
    "suspense": ASSETS_SFX_DIR / "suspense.mp3",
}


def get_sfx_actions(actions: list[dict]) -> list[dict]:
    return [action for action in actions if action.get("type") == "sfx"]


def resolve_sfx_path(name: str) -> Path | None:
    path = SFX_LIBRARY.get(name)

    if path and path.exists():
        return path

    return None