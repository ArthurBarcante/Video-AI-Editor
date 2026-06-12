def calculate_priority_score(highlight: dict) -> float:
    base_score = float(highlight.get("score", 0.0))
    reasons = " ".join(highlight.get("reasons", [])).lower()
    text = highlight.get("text", "").lower()
    duration = highlight["end"] - highlight["start"]

    priority = base_score

    if "alta intensidade" in reasons:
        priority += 0.15

    if "risada" in reasons:
        priority += 0.12

    if "exclamação" in reasons:
        priority += 0.08

    if "palavra-chave" in reasons:
        priority += 0.06

    if any(word in text for word in ["clipa", "não acredito", "meu deus", "caraca"]):
        priority += 0.10

    if 8 <= duration <= 35:
        priority += 0.10

    if duration < 2:
        priority -= 0.30

    if duration > 60:
        priority -= 0.20

    return round(min(max(priority, 0.0), 1.0), 4)


def prioritize_highlights(highlights: list[dict]) -> list[dict]:
    prioritized = []

    for highlight in highlights:
        highlight = highlight.copy()
        highlight["priority_score"] = calculate_priority_score(highlight)
        prioritized.append(highlight)

    return sorted(
        prioritized,
        key=lambda item: item["priority_score"],
        reverse=True,
    )