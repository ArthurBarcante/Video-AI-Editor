def seconds_to_srt_timestamp(seconds: float) -> str:
    milliseconds = int((seconds % 1) * 1000)
    total_seconds = int(seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def seconds_to_ass_timestamp(seconds: float) -> str:
    centiseconds = int((seconds % 1) * 100)
    total_seconds = int(seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    return f"{hours}:{minutes:02}:{secs:02}.{centiseconds:02}"
