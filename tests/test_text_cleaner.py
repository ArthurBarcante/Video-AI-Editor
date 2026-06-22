from src.learning.correction_memory import save_correction_memory
from src.learning.feedback_schema import CorrectionMemory
from src.transcription import text_cleaner


def test_clean_transcript_text_applies_learning_replacements(
    tmp_path,
    monkeypatch,
) -> None:
    corrections_path = tmp_path / "corrections.json"
    save_correction_memory(
        CorrectionMemory(
            transcription_replacements={
                "forte naite": "Fortnite",
            }
        ),
        corrections_path,
    )
    monkeypatch.setattr(
        text_cleaner,
        "apply_transcription_replacements",
        lambda text: text.replace("forte naite", "Fortnite"),
    )

    assert text_cleaner.clean_transcript_text("  jogando forte naite  ") == (
        "jogando Fortnite"
    )
