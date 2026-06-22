from src.learning.correction_memory import (
    add_transcription_replacement,
    load_correction_memory,
    load_learning_profile,
    save_learning_profile,
)
from src.learning.feedback_collector import add_transcription_feedback, load_feedback


def test_add_transcription_replacement_updates_memory(tmp_path) -> None:
    corrections_path = tmp_path / "corrections.json"

    add_transcription_replacement(
        wrong="forte naite",
        correct="Fortnite",
        path=corrections_path,
    )

    memory = load_correction_memory(corrections_path)

    assert memory.transcription_replacements == {"forte naite": "Fortnite"}


def test_add_transcription_feedback_updates_feedback_and_memory(tmp_path) -> None:
    feedback_path = tmp_path / "feedback.json"
    corrections_path = tmp_path / "corrections.json"

    add_transcription_feedback(
        wrong="chat gbt",
        correct="ChatGPT",
        context="nome de ferramenta",
        feedback_path=feedback_path,
        corrections_path=corrections_path,
    )

    feedback = load_feedback(feedback_path)
    memory = load_correction_memory(corrections_path)

    assert feedback.items[0].wrong == "chat gbt"
    assert feedback.items[0].correct == "ChatGPT"
    assert memory.transcription_replacements["chat gbt"] == "ChatGPT"


def test_learning_profile_has_default_editor_preferences(tmp_path) -> None:
    profile_path = tmp_path / "learning_profile.json"
    profile = load_learning_profile(profile_path)
    save_learning_profile(profile, profile_path)
    saved = load_learning_profile(profile_path)

    assert saved.highlights["emotion_weight"] == 0.30
    assert saved.editing["default_zoom_intensity"] == 1.12
    assert saved.subtitles["style"] == "bold_clean"
