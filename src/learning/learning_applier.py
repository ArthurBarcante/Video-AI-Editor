from src.learning.correction_memory import load_correction_memory


def apply_transcription_replacements(text: str) -> str:
    memory = load_correction_memory()

    for wrong, correct in memory.transcription_replacements.items():
        text = text.replace(wrong, correct)

    return text
