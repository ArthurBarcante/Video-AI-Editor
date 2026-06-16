IMPORTANT_TERMS = [
    "boss",
    "final",
    "ganhei",
    "perdi",
    "morri",
    "matei",
    "vitória",
    "derrota",
    "rank",
    "partida",
    "missão",
    "fase",
    "bug",
    "glitch",
    "história",
    "segredo",
    "build",
    "estratégia",
]


def extract_keywords(text: str) -> list[str]:
    text_lower = text.lower()

    return [
        term
        for term in IMPORTANT_TERMS
        if term in text_lower
    ]


def infer_topic(text: str, keywords: list[str]) -> str:
    text_lower = text.lower()

    if any(word in text_lower for word in ["boss", "final", "fase", "missão"]):
        return "progressão de gameplay"

    if any(word in text_lower for word in ["morri", "perdi", "derrota"]):
        return "falha ou derrota"

    if any(word in text_lower for word in ["ganhei", "vitória", "matei"]):
        return "vitória ou conquista"

    if any(word in text_lower for word in ["bug", "glitch"]):
        return "momentos inesperados"

    if any(word in text_lower for word in ["build", "estratégia", "rank"]):
        return "estratégia"

    if keywords:
        return "assunto relevante"

    return "conversa geral"


def calculate_context_importance(text: str, keywords: list[str], topic: str) -> tuple[float, list[str]]:
    score = 0.0
    reasons = []

    if keywords:
        score += min(len(keywords) * 0.12, 0.35)
        reasons.append("termos relevantes detectados")

    if topic != "conversa geral":
        score += 0.25
        reasons.append(f"tópico relevante: {topic}")

    if len(text.split()) >= 20:
        score += 0.10
        reasons.append("bloco com contexto o suficiente")

    if any(word in text.lower() for word in ["primeira vez", "última chance", "não esperava"]):
        score += 0.20
        reasons.append("frase com contexto narrativo")

    return round(min(score, 1.0), 4), reasons
