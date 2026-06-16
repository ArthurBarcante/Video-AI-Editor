SURPRISE_WORDS = [
    "não acredito",
    "que isso",
    "caraca",
    "meu deus",
    "nossa",
    "impossível",
]

ANGER_WORDS = [
    "droga",
    "merda",
    "porra",
    "ódio",
    "não dá",
    "que raiva",
]

JOY_WORDS = [
    "boa",
    "ganhei",
    "consegui",
    "vitória",
    "kkkk",
    "haha",
    "muito bom",
]

HYPE_WORDS = [
    "vamos",
    "bora",
    "clipa",
    "insano",
    "absurdo",
    "lendário",
]


def detect_emotion_from_text(text: str) -> tuple[str, float, list[str]]:
    text_lower = text.lower()

    scores = {
        "surprise": 0.0,
        "anger": 0.0,
        "joy": 0.0,
        "hype": 0.0,
    }

    reasons = []

    for word in SURPRISE_WORDS:
        if word in text_lower:
            scores["surprise"] += 0.25
            reasons.append(f"surpresa: {word}")

    for word in ANGER_WORDS:
        if word in text_lower:
            scores["anger"] += 0.25
            reasons.append(f"raiva: {word}")

    for word in JOY_WORDS:
        if word in text_lower:
            scores["joy"] += 0.25
            reasons.append(f"alegria: {word}")

    for word in HYPE_WORDS:
        if word in text_lower:
            scores["hype"] += 0.25
            reasons.append(f"empolgação: {word}")

    if "!" in text:
        scores["hype"] += 0.12
        scores["surprise"] += 0.08
        reasons.append("exclamação detectada")

    emotion = max(scores, key=scores.get)
    score = min(scores[emotion], 1.0)

    if score == 0:
        return "neutral", 0.0, []

    return emotion, round(score, 4), reasons
