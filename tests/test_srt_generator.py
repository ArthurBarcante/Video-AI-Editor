from pathlib import Path

import pytest

from src.config.paths import ROOT_DIR
from src.subtitles.srt_generator import generate_srt
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
        },
        path,
    )
    return path


def test_generate_srt_from_transcript_json(tmp_path: Path) -> None:
    transcript_path = write_transcript(tmp_path / "live_bruta_transcript.json")
    output_path = tmp_path / "output" / "subtitles" / "live_bruta_transcript.srt"

    srt_path = generate_srt(transcript_path, output_path)
    content = srt_path.read_text(encoding="utf-8")

    assert srt_path == output_path
    assert "1\n00:00:01,500 --> 00:00:03,200\nOlá mundo" in content
    assert "2\n00:00:03,200 --> 00:00:04,000\nPróxima fala" in content


def test_generate_srt_rejects_project_root_output(tmp_path: Path) -> None:
    transcript_path = write_transcript(tmp_path / "transcript.json")

    with pytest.raises(ValueError, match="cache/ ou output"):
        generate_srt(transcript_path, ROOT_DIR / "legend.srt")
