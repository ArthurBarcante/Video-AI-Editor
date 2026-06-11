from pathlib import Path

import pytest

from src.config.paths import ROOT_DIR
from src.subtitles.ass_generator import generate_ass
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


def test_generate_ass_from_transcript_json(tmp_path: Path) -> None:
    transcript_path = write_transcript(tmp_path / "live_bruta_transcript.json")
    output_path = tmp_path / "output" / "subtitles" / "live_bruta_transcript.ass"

    ass_path = generate_ass(transcript_path, output_path)
    content = ass_path.read_text(encoding="utf-8")

    assert ass_path == output_path
    assert "[Script Info]" in content
    assert "Dialogue: 0,0:00:01.50,0:00:03.20,Default,,0,0,0,,Olá mundo" in content
    assert "Dialogue: 0,0:00:03.20,0:00:04.00,Default,,0,0,0,,Próxima fala" in content


def test_generate_ass_rejects_project_root_output(tmp_path: Path) -> None:
    transcript_path = write_transcript(tmp_path / "transcript.json")

    with pytest.raises(ValueError, match="cache/ ou output"):
        generate_ass(transcript_path, ROOT_DIR / "legend.ass")
