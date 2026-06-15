def break_subtitle_text(
    text: str,
    max_chars_per_line: int = 28,
    max_lines: int = 2,
) -> str:
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()

        if len(test_line) <= max_chars_per_line:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

        if len(lines) >= max_lines:
            break

    if current_line and len(lines) < max_lines:
        lines.append(current_line)

    return "\\N".join(lines)
