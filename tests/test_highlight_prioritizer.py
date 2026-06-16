from src.planning.highlight_prioritizer import (
    calculate_priority_score,
    find_context_for_highlight,
    find_emotion_for_highlight,
    prioritize_highlights,
)


def test_short_high_intensity_highlight_keeps_priority() -> None:
    priority_score = calculate_priority_score(
        {
            "start": 10.0,
            "end": 11.5,
            "text": "POOOOO!",
            "score": 0.47,
            "reasons": [
                "exclamação detectada",
                "fala em caixa alta",
                "alta intensidade de áudio",
            ],
        }
    )

    assert priority_score == 0.8


def test_find_context_for_highlight_matches_start_time() -> None:
    highlight = {"start": 125.0, "end": 130.0}
    context_blocks = [
        {"id": "context_001", "start": 0.0, "end": 100.0},
        {"id": "context_002", "start": 120.0, "end": 180.0},
    ]

    assert find_context_for_highlight(highlight, context_blocks) == context_blocks[1]


def test_prioritize_highlights_uses_context_importance() -> None:
    highlights = [
        {
            "start": 125.0,
            "end": 130.0,
            "text": "momento normal",
            "score": 0.4,
            "reasons": [],
        }
    ]
    context_blocks = [
        {
            "id": "context_001",
            "start": 120.0,
            "end": 180.0,
            "importance_score": 0.8,
        }
    ]

    prioritized = prioritize_highlights(highlights, context_blocks=context_blocks)

    assert prioritized[0]["priority_score"] == 0.6
    assert prioritized[0]["context_id"] == "context_001"


def test_find_emotion_for_highlight_matches_start_time() -> None:
    highlight = {"start": 125.0, "end": 130.0}
    emotion_segments = [
        {"start": 0.0, "end": 100.0, "emotion": "neutral"},
        {"start": 120.0, "end": 180.0, "emotion": "surprise"},
    ]

    assert find_emotion_for_highlight(highlight, emotion_segments) == emotion_segments[1]


def test_prioritize_highlights_uses_emotion_score() -> None:
    highlights = [
        {
            "start": 125.0,
            "end": 130.0,
            "text": "momento normal",
            "score": 0.4,
            "reasons": [],
        }
    ]
    emotion_segments = [
        {
            "start": 120.0,
            "end": 180.0,
            "emotion": "surprise",
            "emotion_score": 0.8,
        }
    ]

    prioritized = prioritize_highlights(
        highlights,
        emotion_segments=emotion_segments,
    )

    assert prioritized[0]["priority_score"] == 0.56
    assert prioritized[0]["emotion"] == "surprise"
