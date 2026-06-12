import re


TEXT_LAUGH_PATTERNS = [
    r"\bkkk+\b",
    r"\bhaha+\b",
    r"\brsrs+\b",
    r"\bkkkk+\b",
]


def detect_text_laugh(text: str) -> tuple[float, list[str]]:
    text_lower = text.lower()

    for pattern in TEXT_LAUGH_PATTERNS:
        if re.search(pattern, text_lower):
            return 0.8, ["risada detectada no texto"]

    return 0.0, []


def detect_audio_laugh_by_energy_variation(energy_score: float, text: str) -> tuple[float, list[str]]:
    text_lower = text.lower()

    laugh_words = ["kkk", "haha", "rsrs"]

    if any(word in text_lower for word in laugh_words) and energy_score > 0.45:
        return 0.9, ["risada provável por texto + intensidade de áudio"]

    return 0.0, []