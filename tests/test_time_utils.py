import pytest

from src.utils.time_utils import seconds_to_ass_timestamp, seconds_to_srt_timestamp


def test_seconds_to_srt_timestamp_formats_milliseconds() -> None:
    assert seconds_to_srt_timestamp(1.5) == "00:00:01,500"
    assert seconds_to_srt_timestamp(3.2) == "00:00:03,200"
    assert seconds_to_srt_timestamp(3661.234) == "01:01:01,234"


def test_seconds_to_ass_timestamp_formats_centiseconds() -> None:
    assert seconds_to_ass_timestamp(1.5) == "0:00:01.50"
    assert seconds_to_ass_timestamp(3.2) == "0:00:03.20"
    assert seconds_to_ass_timestamp(3661.234) == "1:01:01.23"


def test_timestamp_helpers_reject_negative_values() -> None:
    with pytest.raises(ValueError, match="não pode ser negativo"):
        seconds_to_srt_timestamp(-0.1)

    with pytest.raises(ValueError, match="não pode ser negativo"):
        seconds_to_ass_timestamp(-0.1)
