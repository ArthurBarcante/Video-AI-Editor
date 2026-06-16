def group_segments_into_blocks(
    segments: list[dict],
    max_gap: float = 8.0,
    max_duration: float = 90.0,
) -> list[dict]:
    blocks = []
    current = None

    for segment in segments:
        if not segment.get("text", "").strip():
            continue

        if current is None:
            current = {
                "start": segment["start"],
                "end": segment["end"],
                "texts": [segment["text"]],
            }
            continue

        gap = segment["start"] - current["end"]
        duration = segment["end"] - current["start"]

        if gap <= max_gap and duration <= max_duration:
            current["end"] = segment["end"]
            current["texts"].append(segment["text"])
        else:
            blocks.append(current)
            current = {
                "start": segment["start"],
                "end": segment["end"],
                "texts": [segment["text"]],
            }

    if current:
        blocks.append(current)

    return blocks
