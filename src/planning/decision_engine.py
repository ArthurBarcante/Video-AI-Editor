def should_be_short(highlight: dict) -> bool:
    score = highlight["score"]
    duration = highlight["end"] - highlight["start"]

    if score < 0.55:
        return False

    if duration < 2:
        return False

    return True


def should_be_long_segment(highlight: dict) -> bool:
    score = highlight["score"]
    duration = highlight["end"] - highlight["start"]

    if score < 0.35:
        return False

    if duration < 2:
        return False

    return True


def choose_edit_style(highlight: dict) -> str:
    reasons = " ".join(highlight.get("reasons", [])).lower()
    text = highlight.get("text", "").lower()

    if "risada" in reasons or "kkk" in text:
        return "funny"

    if "alta intensidade" in reasons or "exclamação" in reasons:
        return "intense"

    if "palavra-chave" in reasons:
        return "highlight"

    return "default"


def generate_actions_for_highlight(highlight: dict) -> list[dict]:
    actions = []

    reasons = " ".join(highlight.get("reasons", [])).lower()

    if "alta intensidade" in reasons:
        actions.append(
            {
                "type": "zoom",
                "start": highlight["start"],
                "end": min(highlight["start"] + 2.5, highlight["end"]),
                "intensity": 1.2,
                "target": "center",
            }
        )

    if "risada" in reasons:
        actions.append(
            {
                "type": "sfx",
                "time": highlight["start"],
                "name": "pop",
            }
        )

    if "exclamação" in reasons:
        actions.append(
            {
                "type": "subtitle_emphasis",
                "start": highlight["start"],
                "end": highlight["end"],
                "style": "impact",
            }
        )

    return actions
