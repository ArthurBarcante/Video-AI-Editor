def should_be_short(highlight: dict) -> bool:
    score = highlight.get("priority_score", highlight["score"])
    duration = highlight["end"] - highlight["start"]
    reasons = " ".join(highlight.get("reasons", [])).lower()

    if score <= 0.50:
        return False

    if duration >= 1 and (
        "alta intensidade" in reasons
        or "risada" in reasons
    ):
        return True

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
    reasons = " ".join(highlight.get("reasons", [])).lower()
    text = highlight.get("text", "").lower()
    actions = []

    if "alta intensidade" in reasons:
        actions.extend(
            [
                {
                    "type": "zoom",
                    "intensity": 1.25,
                    "target": "center",
                    "reason": "zoom por alta intensidade",
                },
                {
                    "type": "sfx",
                    "time": highlight["start"],
                    "name": "impact",
                    "volume": 0.35,
                    "reason": "sfx por alta intensidade",
                },
            ]
        )

        return actions

    if "risada" in reasons:
        actions.extend(
            [
                {
                    "type": "zoom",
                    "intensity": 1.18,
                    "target": "center",
                    "reason": "zoom por reação/risada",
                },
                {
                    "type": "sfx",
                    "time": highlight["start"],
                    "name": "laugh",
                    "volume": 0.25,
                    "reason": "sfx por risada",
                },
            ]
        )

        return actions

    if any(word in text for word in ["mano", "caraca", "meu deus", "não acredito"]):
        actions.extend(
            [
                {
                    "type": "zoom",
                    "intensity": 1.15,
                    "target": "center",
                    "reason": "zoom por palavra-chave",
                },
                {
                    "type": "sfx",
                    "time": highlight["start"],
                    "name": "pop",
                    "volume": 0.25,
                    "reason": "sfx por palavra-chave",
                },
            ]
        )

        return actions

    if "exclamação" in reasons:
        return [
            {
                "type": "sfx",
                "time": highlight["start"],
                "name": "pop",
                "volume": 0.2,
                "reason": "sfx por exclamação",
            },
        ]

    return []
