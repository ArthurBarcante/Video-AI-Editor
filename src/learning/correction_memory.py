from pathlib import Path

from src.config.paths import CACHE_LEARNING_DIR
from src.learning.feedback_schema import CorrectionMemory, LearningProfile
from src.utils.file_utils import load_json, save_json


CORRECTIONS_PATH = CACHE_LEARNING_DIR / "corrections.json"
LEARNING_PROFILE_PATH = CACHE_LEARNING_DIR / "learning_profile.json"
SUCCESSFUL_PATTERNS_PATH = CACHE_LEARNING_DIR / "successful_patterns.json"


def load_correction_memory(path: str | Path = CORRECTIONS_PATH) -> CorrectionMemory:
    path = Path(path)

    if not path.exists():
        return CorrectionMemory()

    return CorrectionMemory.model_validate(load_json(path))


def save_correction_memory(
    memory: CorrectionMemory,
    path: str | Path = CORRECTIONS_PATH,
) -> Path:
    path = Path(path)
    save_json(memory.model_dump(), path)
    return path


def add_transcription_replacement(
    wrong: str,
    correct: str,
    path: str | Path = CORRECTIONS_PATH,
) -> Path:
    memory = load_correction_memory(path)
    memory.transcription_replacements[wrong] = correct
    return save_correction_memory(memory, path)


def load_learning_profile(path: str | Path = LEARNING_PROFILE_PATH) -> LearningProfile:
    path = Path(path)

    if not path.exists():
        return LearningProfile()

    return LearningProfile.model_validate(load_json(path))


def save_learning_profile(
    profile: LearningProfile,
    path: str | Path = LEARNING_PROFILE_PATH,
) -> Path:
    path = Path(path)
    save_json(profile.model_dump(), path)
    return path


def ensure_learning_files() -> None:
    from src.learning.feedback_collector import load_feedback, save_feedback

    memory = load_correction_memory()
    profile = load_learning_profile()
    feedback = load_feedback()

    save_correction_memory(memory)
    save_learning_profile(profile)
    save_feedback(feedback)

    if not SUCCESSFUL_PATTERNS_PATH.exists():
        save_json({"patterns": []}, SUCCESSFUL_PATTERNS_PATH)
