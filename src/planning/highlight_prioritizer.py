def find_context_for_highlight(highlight: dict, context_blocks: list[dict]) -> dict | None:
    highlight_start = highlight["start"]

    for block in context_blocks:
        if block["start"] <= highlight_start <= block["end"]:
            return block

    return None


def find_emotion_for_highlight(highlight: dict, emotion_segments: list[dict]) -> dict | None:
    highlight_start = highlight["start"]

    for segment in emotion_segments:
        if segment["start"] <= highlight_start <= segment["end"]:
            return segment

    return None


def calculate_priority_score(
    highlight: dict,
    context: dict | None = None,
    emotion: dict | None = None,
) -> float:
    base_score = float(highlight.get("score", 0.0))
    reasons = " ".join(highlight.get("reasons", [])).lower()
    text = highlight.get("text", "").lower()
    duration = highlight["end"] - highlight["start"]
    has_strong_event = "alta intensidade" in reasons or "risada" in reasons

    priority = base_score

    if "alta intensidade" in reasons:
        priority += 0.25

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

    if duration < 2 and not has_strong_event:
        priority -= 0.30

    if duration > 60:
        priority -= 0.20

    if context:
        priority += float(context.get("importance_score", 0.0)) * 0.25

    if emotion:
        emotion_name = emotion.get("emotion")
        emotion_score = float(emotion.get("emotion_score", 0.0))

        if emotion_name in ["surprise", "hype", "joy"]:
            priority += emotion_score * 0.20
        elif emotion_name == "anger":
            priority += emotion_score * 0.10

    return round(min(max(priority, 0.0), 1.0), 4)


def prioritize_highlights(
    highlights: list[dict],
    context_blocks: list[dict] | None = None,
    emotion_segments: list[dict] | None = None,
) -> list[dict]:
    context_blocks = context_blocks or []
    emotion_segments = emotion_segments or []
    prioritized = []

    for highlight in highlights:
        context = find_context_for_highlight(highlight, context_blocks)
        emotion = find_emotion_for_highlight(highlight, emotion_segments)
        highlight = highlight.copy()
        highlight["priority_score"] = calculate_priority_score(
            highlight,
            context=context,
            emotion=emotion,
        )

        if context:
            highlight["context_id"] = context["id"]

        if emotion:
            highlight["emotion"] = emotion["emotion"]

        prioritized.append(highlight)

    return sorted(
        prioritized,
        key=lambda item: item["priority_score"],
        reverse=True,
    )
