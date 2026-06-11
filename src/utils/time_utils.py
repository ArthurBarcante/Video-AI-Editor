def seconds_to_srt_timestamp(seconds: float) -> str:
    if seconds < 0:
        raise ValueError("Timestamp não pode ser negativo")

    total_milliseconds = round(seconds * 1000)
    total_seconds, milliseconds = divmod(total_milliseconds, 1000)

    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def seconds_to_ass_timestamp(seconds: float) -> str:
    if seconds < 0:
        raise ValueError("Timestamp não pode ser negativo")

    total_centiseconds = round(seconds * 100)
    total_seconds, centiseconds = divmod(total_centiseconds, 100)

    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    return f"{hours}:{minutes:02}:{secs:02}.{centiseconds:02}"
