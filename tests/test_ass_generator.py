from pathlib import Path

import pytest

from src.config.paths import ROOT_DIR
from src.subtitles.ass_generator import generate_ass, generate_short_ass_files
from src.utils.file_utils import save_json


def write_transcript(path: Path) -> Path:
    save_json(
        {
            "source_audio": "cache/audio/live_bruta.wav",
            "language": "pt",
            "duration": 3.2,
            "segments": [
                {"start": 1.5, "end": 3.2, "text": "Olá mundo"},
                {"start": 3.2, "end": 4.0, "text": "Próxima fala"},
            ],
            "metadata": {
                "execution_time_seconds": 1.0,
                "audio_duration_seconds": 3.2,
                "realtime_speed": 3.2,
                "segment_count": 2,
                "model": "tiny",
                "device": "cpu",
                "compute_type": "int8",
                "beam_size": 1,
                "best_of": 1,
                "vad_filter": True,
                "word_timestamps": False,
                "profile": "fast",
            },
        },
        path,
    )
    return path


def test_generate_ass_from_transcript_json(tmp_path: Path) -> None:
    transcript_path = write_transcript(tmp_path / "live_bruta_transcript.json")
    output_path = tmp_path / "output" / "subtitles" / "live_bruta_transcript.ass"

    ass_path = generate_ass(transcript_path, output_path)
    content = ass_path.read_text(encoding="utf-8")

    assert ass_path == output_path
    assert "[Script Info]" in content
    assert "Dialogue: 0,0:00:01.50,0:00:03.20,Default,,0,0,0,,Olá mundo" in content
    assert "Dialogue: 0,0:00:03.20,0:00:04.20,Default,,0,0,0,,Próxima fala" in content


def test_generate_ass_short_mode_formats_for_shorts(tmp_path: Path) -> None:
    transcript_path = write_transcript(tmp_path / "short_transcript.json")
    output_path = tmp_path / "output" / "subtitles" / "short_transcript_short.ass"

    ass_path = generate_ass(transcript_path, output_path, mode="short")
    content = ass_path.read_text(encoding="utf-8")

    assert ass_path == output_path
    assert "Video AI Editor Shorts Subtitles" in content
    assert "Montserrat ExtraBold,70" in content
    assert ",1,4,0,2," in content
    assert "{\\c&H00FFFF&\\b1}" not in content


def test_generate_ass_short_mode_keeps_clean_text_without_word_highlights(
    tmp_path: Path,
) -> None:
    transcript_path = tmp_path / "highlight_transcript.json"
    save_json(
        {
            "source_audio": "cache/audio/live_bruta.wav",
            "language": "pt",
            "duration": 4.0,
            "segments": [
                {"start": 1.0, "end": 4.0, "text": "Mano, olha isso agora!"},
            ],
            "metadata": {
                "execution_time_seconds": 1.0,
                "audio_duration_seconds": 4.0,
                "realtime_speed": 4.0,
                "segment_count": 1,
                "model": "tiny",
                "device": "cpu",
                "compute_type": "int8",
                "beam_size": 1,
                "best_of": 1,
                "vad_filter": True,
                "word_timestamps": False,
                "profile": "fast",
            },
        },
        transcript_path,
    )
    output_path = tmp_path / "output" / "subtitles" / "highlight_transcript_short.ass"

    ass_path = generate_ass(transcript_path, output_path, mode="short")
    content = ass_path.read_text(encoding="utf-8")

    assert "Mano, olha isso agora!" in content
    assert "{\\c&H00FFFF&\\b1}" not in content


def test_generate_short_ass_files_filters_and_offsets_segments(tmp_path: Path) -> None:
    transcript_path = tmp_path / "live_transcript.json"
    edit_plan_path = tmp_path / "edit_plan.json"
    output_dir = tmp_path / "output" / "subtitles"

    save_json(
        {
            "source_audio": "cache/audio/live_bruta.wav",
            "language": "pt",
            "duration": 20.0,
            "segments": [
                {"start": 9.0, "end": 10.0, "text": "antes"},
                {"start": 12.0, "end": 14.5, "text": "mano mano olha isso"},
                {"start": 18.5, "end": 20.0, "text": "depois"},
            ],
            "metadata": {
                "execution_time_seconds": 1.0,
                "audio_duration_seconds": 20.0,
                "realtime_speed": 20.0,
                "segment_count": 3,
                "model": "tiny",
                "device": "cpu",
                "compute_type": "int8",
                "beam_size": 1,
                "best_of": 1,
                "vad_filter": True,
                "word_timestamps": False,
                "profile": "fast",
            },
        },
        transcript_path,
    )
    save_json(
        {
            "source_video": "input/live_bruta.mp4",
            "shorts": [
                {
                    "id": "short_01",
                    "start": 10.0,
                    "end": 18.0,
                    "duration": 8.0,
                    "score": 0.8,
                    "title": "MANO OLHA ISSO",
                    "reason": "teste",
                    "style": "highlight",
                    "actions": [],
                }
            ],
            "long_videos": [],
        },
        edit_plan_path,
    )

    paths = generate_short_ass_files(
        transcript_path=transcript_path,
        edit_plan_path=edit_plan_path,
        output_dir=output_dir,
    )
    content = paths[0].read_text(encoding="utf-8")

    assert paths == [output_dir / "short_01.ass"]
    assert "Dialogue: 0,0:00:02.00,0:00:03.67,Default,,0,0,0,,Mano olha" in content
    assert "Dialogue: 0,0:00:03.67,0:00:04.50,Default,,0,0,0,,isso" in content
    assert "antes" not in content
    assert "depois" not in content


def test_generate_ass_rejects_invalid_mode(tmp_path: Path) -> None:
    transcript_path = write_transcript(tmp_path / "transcript.json")

    with pytest.raises(ValueError, match="Modo ASS inválido"):
        generate_ass(transcript_path, mode="vertical")


def test_generate_ass_rejects_project_root_output(tmp_path: Path) -> None:
    transcript_path = write_transcript(tmp_path / "transcript.json")

    with pytest.raises(ValueError, match="cache/ ou output"):
        generate_ass(transcript_path, ROOT_DIR / "legend.ass")
