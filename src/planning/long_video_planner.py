from src.config.settings import (
    LONG_VIDEO_MAX_DURATION,
    LONG_VIDEO_MIN_DURATION,
    MAX_LONG_VIDEOS,
)
from src.planning.decision_engine import should_be_long_segment
from src.planning.edit_plan_schema import LongVideoPlan, LongVideoSegment


MIN_LONG_VIDEO_EXPORT_DURATION = 60


def expand_long_segment(start: float, end: float) -> tuple[float, float]:
    padding_before = 8
    padding_after = 8

    start = max(0, start - padding_before)
    end = end + padding_after

    return round(start, 2), round(end, 2)


def plan_long_video_segments(highlights: list[dict]) -> list[LongVideoSegment]:
    segments = []
    total_duration = 0.0

    candidates = [
        highlight
        for highlight in highlights
        if should_be_long_segment(highlight)
    ]

    candidates = sorted(
        candidates,
        key=lambda item: item.get("priority_score", item["score"]),
        reverse=True,
    )

    candidates = candidates[:80]

    candidates = sorted(candidates, key=lambda item: item["start"])

    for highlight in candidates:
        if total_duration >= LONG_VIDEO_MAX_DURATION:
            break

        start, end = expand_long_segment(
            highlight["start"],
            highlight["end"],
        )

        duration = round(end - start, 2)

        if total_duration + duration > LONG_VIDEO_MAX_DURATION:
            continue

        segment = LongVideoSegment(
            start=start,
            end=end,
            duration=duration,
            score=highlight["score"],
            reason=", ".join(highlight.get("reasons", [])),
        )

        segments.append(segment)
        total_duration += duration

    return segments


def plan_long_videos(highlights: list[dict]) -> list[LongVideoPlan]:
    long_videos = []

    for index in range(1, MAX_LONG_VIDEOS + 1):
        segments = plan_long_video_segments(highlights)

        total_duration = sum(segment.duration for segment in segments)

        if total_duration < MIN_LONG_VIDEO_EXPORT_DURATION:
            continue

        if total_duration < LONG_VIDEO_MIN_DURATION:
            title = "Melhores momentos da live"
            theme = "compilado curto de melhores momentos"
        else:
            title = "Melhores momentos da live"
            theme = "melhores momentos"

        long_video = LongVideoPlan(
            id=f"video_{index:02}",
            title=title,
            duration_target=LONG_VIDEO_MIN_DURATION,
            theme=theme,
            segments=segments,
            actions=[],
        )

        long_videos.append(long_video)

    return long_videos
