import math

from src.transcription.subtitle_cleaner import SubtitleSegment, clean_subtitle_text
from src.transcription.transcript_schema import Transcript, TranscriptSegment


SHORT_MAX_WORDS = 5
SHORT_MAX_DURATION = 2.2


def _as_segment_list(transcript: Transcript | list[TranscriptSegment]) -> list[TranscriptSegment]:
    if isinstance(transcript, Transcript):
        return transcript.segments

    return transcript


def filter_segments_by_range(
    transcript: Transcript | list[TranscriptSegment],
    start: float,
    end: float,
) -> list[TranscriptSegment]:
    segments = _as_segment_list(transcript)

    return [
        segment
        for segment in segments
        if segment.end > start and segment.start < end
    ]


def shift_segments_to_zero(
    segments: list[TranscriptSegment],
    start: float,
    end: float,
) -> list[SubtitleSegment]:
    duration = end - start
    shifted = []

    for segment in segments:
        text = clean_subtitle_text(segment.text)

        if not text:
            continue

        shifted_start = round(max(0.0, segment.start - start), 3)
        shifted_end = round(min(duration, segment.end - start), 3)

        if shifted_end <= shifted_start:
            continue

        shifted.append(
            SubtitleSegment(
                start=shifted_start,
                end=shifted_end,
                text=text,
            )
        )

    return shifted


def _split_words_by_group(words: list[str], group_size: int) -> list[list[str]]:
    return [
        words[index : index + group_size]
        for index in range(0, len(words), group_size)
    ]


def _split_words_balanced(words: list[str], group_count: int) -> list[list[str]]:
    if group_count <= 1:
        return [words]

    groups = []
    total_words = len(words)
    cursor = 0

    for index in range(group_count):
        remaining_words = total_words - cursor
        remaining_groups = group_count - index
        group_size = math.ceil(remaining_words / remaining_groups)

        groups.append(words[cursor : cursor + group_size])
        cursor += group_size

    return [group for group in groups if group]


def split_long_segments(
    segments: list[SubtitleSegment],
    max_words: int = SHORT_MAX_WORDS,
    max_duration: float = SHORT_MAX_DURATION,
) -> list[SubtitleSegment]:
    split_segments = []

    for segment in segments:
        words = segment.text.split()
        duration = round(segment.end - segment.start, 3)

        if len(words) <= max_words and duration <= max_duration:
            split_segments.append(segment)
            continue

        word_groups = _split_words_by_group(words, max_words)
        group_count = max(
            len(word_groups),
            math.ceil(duration / max_duration),
        )

        word_groups = _split_words_balanced(words, group_count)

        seconds_per_word = duration / max(len(words), 1)
        cursor = segment.start

        for group in word_groups:
            group_duration = seconds_per_word * len(group)
            group_end = round(min(segment.end, cursor + group_duration), 3)

            split_segments.append(
                SubtitleSegment(
                    start=round(cursor, 3),
                    end=group_end,
                    text=" ".join(group),
                )
            )
            cursor = group_end

    return split_segments


def get_segments_for_range(
    transcript: Transcript | list[TranscriptSegment],
    start: float,
    end: float,
) -> list[SubtitleSegment]:
    segments = filter_segments_by_range(transcript, start, end)
    shifted = shift_segments_to_zero(segments, start, end)
    return split_long_segments(shifted)
