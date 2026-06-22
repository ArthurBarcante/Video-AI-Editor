from src.subtitles.line_breaker import smart_line_break


def test_smart_line_break_prefers_connector_words() -> None:
    text = "eu estava andando na rua quando encontrei um cara"

    assert smart_line_break(text) == (
        "eu estava andando na rua\\Nquando encontrei um cara"
    )


def test_smart_line_break_keeps_short_text_on_one_line() -> None:
    assert smart_line_break("Mano olha isso") == "Mano olha isso"
