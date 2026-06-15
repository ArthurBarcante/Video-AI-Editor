from src.planning.highlight_prioritizer import calculate_priority_score


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
