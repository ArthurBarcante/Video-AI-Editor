import re


IMPORTANT_WORDS = [
    "mano",
    "caraca",
    "não acredito",
    "meu deus",
    "que isso",
    "clipa",
    "olha isso",
]


def highlight_important_words(text: str) -> str:
    highlighted = text

    for word in IMPORTANT_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        highlighted = pattern.sub(
            lambda match: (
                "{\\c&H00FFFF&\\b1}"
                f"{match.group(0)}"
                "{\\c&HFFFFFF&\\b0}"
            ),
            highlighted,
        )

    return highlighted
