def select_thumbnail_timestamp(item: dict) -> float:
    start = float(item["start"])
    end = float(item["end"])

    return start + ((end - start) / 2)


def select_best_shorts_for_thumbnails(shorts: list[dict]) -> list[dict]:
    return sorted(
        shorts,
        key=lambda item: item.get("score", 0),
        reverse=True,
    )
