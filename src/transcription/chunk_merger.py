def merge_chunk_segments(chunk_results: list[dict]) -> list[dict]:
    all_segments = []

    for chunk in chunk_results:
        all_segments.extend(chunk.get("segments", []))

    all_segments = sorted(all_segments, key=lambda item: item["start"])

    merged = []
    last_text = None
    last_end = -1.0

    for segment in all_segments:
        text = segment["text"].strip()

        if not text:
            continue

        is_duplicate = (
            last_text == text
            and abs(segment["start"] - last_end) <= 3
        )

        if is_duplicate:
            continue

        merged.append(segment)
        last_text = text
        last_end = segment["end"]

    return merged
