import re

from src.learning.learning_applier import apply_transcription_replacements

REPLACEMENTS = {
    " neh ": " né ",
    " ta ": " tá ",
    " voce ": " você ",
    " nao ": " não ",
    " mano mano": "mano",
}


def clean_transcript_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    for wrong, right in REPLACEMENTS.items():
        text = text.replace(wrong, right)

    text = apply_transcription_replacements(text)

    return text
