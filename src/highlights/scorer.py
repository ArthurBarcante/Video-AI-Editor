KEYWORDS = [
    "mano",
    "caraca",
    "não acredito",
    "que isso",
    "clipa",
    "olha isso",
    "meu deus",
    "nossa",
    "calma",
    "pera",
]


def score_highlight(
    text: str,
    energy_score: float = 0.0,
    laugh_score: float = 0.0,
) -> tuple[float, list[str]]:
    text_lower = text.lower()

    score = 0.0
    reasons = []

    for keyword in KEYWORDS:
        if keyword in text_lower:
            score += 0.18
            reasons.append(f"palavra-chave: {keyword}")

    if "!" in text:
        score += 0.12
        reasons.append("exclamação detectada")

    if text.isupper() and len(text) > 5:
        score += 0.10
        reasons.append("fala em caixa alta")

    word_count = len(text.split())

    if 3 <= word_count <= 18:
        score += 0.10
        reasons.append("fala curta com potencial de corte")

    if energy_score >= 0.70:
        score += 0.25
        reasons.append("alta intensidade de áudio")
    elif energy_score >= 0.45:
        score += 0.15
        reasons.append("intensidade média de áudio")

    if laugh_score >= 0.70:
        score += 0.22
        reasons.append("risada detectada")

    return round(min(score, 1.0), 2), reasons
