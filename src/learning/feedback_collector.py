from pathlib import Path

from src.config.paths import CACHE_LEARNING_DIR
from src.learning.correction_memory import add_transcription_replacement
from src.learning.feedback_schema import FeedbackLog, TranscriptionCorrection
from src.utils.file_utils import load_json, save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)

FEEDBACK_PATH = CACHE_LEARNING_DIR / "feedback.json"


def load_feedback(path: str | Path = FEEDBACK_PATH) -> FeedbackLog:
    path = Path(path)

    if not path.exists():
        return FeedbackLog()

    return FeedbackLog.model_validate(load_json(path))


def save_feedback(feedback: FeedbackLog, path: str | Path = FEEDBACK_PATH) -> Path:
    path = Path(path)
    save_json(feedback.model_dump(), path)
    return path


def add_transcription_feedback(
    wrong: str,
    correct: str,
    context: str = "",
    apply_future: bool = True,
    feedback_path: str | Path = FEEDBACK_PATH,
    corrections_path: str | Path | None = None,
) -> Path:
    feedback = load_feedback(feedback_path)
    item = TranscriptionCorrection(
        wrong=wrong,
        correct=correct,
        context=context,
        apply_future=apply_future,
    )
    feedback.items.append(item)
    output_path = save_feedback(feedback, feedback_path)

    if apply_future:
        if corrections_path is None:
            add_transcription_replacement(wrong, correct)
        else:
            add_transcription_replacement(wrong, correct, corrections_path)

    logger.info("Feedback de transcrição registrado: %s -> %s", wrong, correct)

    return output_path
