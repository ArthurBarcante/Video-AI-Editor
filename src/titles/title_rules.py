POWER_WORDS = [
    "INSANO",
    "INACREDITÁVEL",
    "ABSURDO",
    "ÉPICO",
    "IMPRESSIONANTE",
]


def clean_title_text(text: str) -> str:
    text = text.strip().replace("\n", " ")

    if len(text) > 55:
        text = text[:52] + "..."

    return text.upper()


def generate_title_variants(text: str, style: str = "highlight") -> list[str]:
    base = clean_title_text(text)

    if style == "funny":
        return [
            "EU NÃO TAVA ESPERANDO ISSO 😂",
            "ESSE MOMENTO ME QUEBROU",
            base,
        ]

    if style == "intense":
        return [
            "ISSO FOI ABSURDO!",
            "EU NÃO ACREDITO QUE ISSO ACONTECEU",
            base,
        ]

    return [
        base,
        "MELHOR MOMENTO DA LIVE",
        "ISSO ACONTECEU AO VIVO",
    ]


def score_title(title: str) -> float:
    score = 0.4

    if 25 <= len(title) <= 60:
        score += 0.2

    if any(word in title for word in POWER_WORDS):
        score += 0.2

    if "!" in title:
        score += 0.1

    if any(word in title for word in ["NÃO ACREDITO", "AO VIVO", "MELHOR"]):
        score += 0.1

    if title == "EU NÃO ACREDITO QUE ISSO ACONTECEU":
        score += 0.1

    return round(min(score, 1.0), 4)
