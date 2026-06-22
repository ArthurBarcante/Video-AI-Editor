BREAK_WORDS = {
    "e",
    "mas",
    "porque",
    "quando",
}


def _join_lines(lines: list[str]) -> str:
    return "\\N".join(line.strip() for line in lines if line.strip())


def _split_at_best_point(text: str, max_chars_per_line: int) -> list[str]:
    if len(text) <= max_chars_per_line:
        return [text]

    middle = len(text) // 2
    candidates = []

    for index, char in enumerate(text):
        if char in ",.!?":
            candidates.append(index + 1)

    words = text.split()
    cursor = 0

    for word in words[:-1]:
        cursor += len(word)
        clean_word = word.strip(",.!?").lower()

        if clean_word in BREAK_WORDS:
            candidates.append(cursor - len(word))

        cursor += 1

    valid_candidates = [
        candidate
        for candidate in candidates
        if 0 < candidate < len(text)
        and len(text[:candidate].strip()) <= max_chars_per_line
        and len(text[candidate:].strip()) <= max_chars_per_line
    ]

    if valid_candidates:
        split_at = min(valid_candidates, key=lambda candidate: abs(candidate - middle))
        return [text[:split_at].strip(" ,"), text[split_at:].strip()]

    words = text.split()
    first_line = ""
    second_line = ""

    for word in words:
        test_line = f"{first_line} {word}".strip()

        if len(test_line) <= max_chars_per_line or not first_line:
            first_line = test_line
        else:
            second_line = f"{second_line} {word}".strip()

    return [first_line, second_line]


def smart_line_break(
    text: str,
    max_chars_per_line: int = 42,
    max_lines: int = 2,
) -> str:
    text = " ".join(text.split())

    if max_lines <= 1 or len(text) <= max_chars_per_line:
        return text

    lines = _split_at_best_point(text, max_chars_per_line)

    if len(lines) <= max_lines:
        return _join_lines(lines)

    return _join_lines(lines[:max_lines])


def break_subtitle_text(
    text: str,
    max_chars_per_line: int = 42,
    max_lines: int = 2,
) -> str:
    return smart_line_break(text, max_chars_per_line, max_lines)
