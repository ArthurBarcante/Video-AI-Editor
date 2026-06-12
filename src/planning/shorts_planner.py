from src.config.settings import MAX_SHORTS, SHORT_MAX_DURATION, SHORT_MIN_DURATION
from src.planning.decision_engine import (
    choose_edit_style,
    generate_actions_for_highlight,
    should_be_short,
)
from src.planning.edit_plan_schema import ShortPlan


def expand_short_window(start: float, end: float) -> tuple[float, float]:
    duration = end - start

    if duration < SHORT_MIN_DURATION:
        end = start + SHORT_MIN_DURATION

    if end - start > SHORT_MAX_DURATION:
        end = start + SHORT_MAX_DURATION

    return round(start, 2), round(end, 2)


def make_short_title(text: str) -> str:
    clean = text.strip()

    if not clean:
        return "MELHOR MOMENTO"

    if len(clean) > 60:
        clean = clean[:57] + "..."

    return clean.upper()


def plan_shorts(highlights: list[dict]) -> list[ShortPlan]:
    candidates = [
        highlight
        for highlight in highlights
        if should_be_short(highlight)
    ]

    candidates = sorted(
        candidates,
        key=lambda item: item.get("priority_score", item["score"]),
        reverse=True,
    )

    shorts = []

    for index, highlight in enumerate(candidates[:MAX_SHORTS], start=1):
        start, end = expand_short_window(
            highlight["start"],
            highlight["end"],
        )

        short = ShortPlan(
            id=f"short_{index:02}",
            start=start,
            end=end,
            duration=round(end - start, 2),
            score=highlight.get("priority_score", highlight["score"]),
            title=make_short_title(highlight.get("text", "")),
            reason=", ".join(highlight.get("reasons", [])),
            style=choose_edit_style(highlight),
            actions=generate_actions_for_highlight(highlight),
        )

        shorts.append(short)

    return shorts
