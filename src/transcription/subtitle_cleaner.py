import math
import re
from dataclasses import dataclass

from src.transcription.transcript_schema import TranscriptSegment


MIN_SUBTITLE_DURATION = 1.0
MAX_SUBTITLE_DURATION = 6.0

HESITATION_WORDS = {
    "ah",
    "aham",
    "eh",
    "é",
    "hã",
    "hum",
    "uh",
}


@dataclass(frozen=True)
class SubtitleSegment:
    start: float
    end: float
    text: str


def _capitalize_first(text: str) -> str:
    if not text:
        return text

    return f"{text[0].upper()}{text[1:]}"


def _normalize_elongated_words(text: str) -> str:
    text = re.sub(r"\ba+h+\b", "Ah", text, flags=re.IGNORECASE)
    return re.sub(r"([A-Za-zÀ-ÿ])\1{3,}", r"\1", text)


def _collapse_repeated_words(text: str) -> str:
    words = text.split()
    collapsed = []

    for word in words:
        clean_word = re.sub(r"[^\wÀ-ÿ]", "", word).lower()
        previous = collapsed[-1] if collapsed else ""
        previous_clean = re.sub(r"[^\wÀ-ÿ]", "", previous).lower()

        if clean_word and clean_word == previous_clean:
            continue

        collapsed.append(word)

    return " ".join(collapsed)


def _remove_initial_hesitations(text: str) -> str:
    words = text.split()

    while len(words) > 1:
        clean_word = re.sub(r"[^\wÀ-ÿ]", "", words[0]).lower()

        if clean_word not in HESITATION_WORDS:
            break

        words.pop(0)

    return " ".join(words)


def clean_subtitle_text(text: str) -> str:
    text = text.strip().replace("\n", " ")
    text = re.sub(r"\.{2,}", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = _normalize_elongated_words(text)
    text = _collapse_repeated_words(text)
    text = _remove_initial_hesitations(text)
    text = re.sub(r"\s+", " ", text).strip(" ,")

    return _capitalize_first(text)


def _split_text_evenly(text: str, parts: int) -> list[str]:
    words = text.split()

    if not words:
        return [text] * parts

    chunk_size = max(1, math.ceil(len(words) / parts))
    chunks = [
        " ".join(words[index : index + chunk_size])
        for index in range(0, len(words), chunk_size)
    ]

    while len(chunks) < parts:
        chunks.append(chunks[-1])

    return chunks[:parts]


def prepare_subtitle_segments(
    segments: list[TranscriptSegment],
    window_start: float | None = None,
    window_end: float | None = None,
) -> list[SubtitleSegment]:
    prepared = []

    for segment in segments:
        start = segment.start
        end = segment.end
        max_window_end = None

        if window_start is not None and end <= window_start:
            continue

        if window_end is not None and start >= window_end:
            continue

        if window_start is not None:
            start = max(start, window_start)

        if window_end is not None:
            end = min(end, window_end)
            max_window_end = window_end

        if window_start is not None:
            start -= window_start
            end -= window_start
            if max_window_end is not None:
                max_window_end -= window_start

        text = clean_subtitle_text(segment.text)

        if not text:
            continue

        duration = end - start

        if duration <= 0:
            continue

        if duration > MAX_SUBTITLE_DURATION:
            parts = math.ceil(duration / MAX_SUBTITLE_DURATION)
            part_duration = duration / parts
            text_parts = _split_text_evenly(text, parts)

            for index in range(parts):
                part_start = start + (part_duration * index)
                part_end = start + (part_duration * (index + 1))
                prepared.append(
                    SubtitleSegment(
                        start=part_start,
                        end=part_end,
                        text=text_parts[index],
                    )
                )

            continue

        if duration < MIN_SUBTITLE_DURATION:
            end = start + MIN_SUBTITLE_DURATION
            if max_window_end is not None:
                end = min(end, max_window_end)

        prepared.append(SubtitleSegment(start=start, end=end, text=text))

    return prepared
