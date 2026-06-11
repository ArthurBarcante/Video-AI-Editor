import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from src.config.paths import (
    CACHE_AUDIO_DIR,
    CACHE_TRANSCRIPTS_DIR,
    INPUT_DIR,
    OUTPUT_SUBTITLES_DIR,
    ROOT_DIR,
)
from src.utils.file_utils import save_json


def test_python_main_runs_phase_3_in_expected_order(sample_video: Path) -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    input_video = INPUT_DIR / "000_pytest_phase3.mp4"
    audio_output = CACHE_AUDIO_DIR / "000_pytest_phase3.wav"
    transcript_output = CACHE_TRANSCRIPTS_DIR / "000_pytest_phase3_transcript.json"
    srt_output = OUTPUT_SUBTITLES_DIR / "000_pytest_phase3_transcript.srt"
    ass_output = OUTPUT_SUBTITLES_DIR / "000_pytest_phase3_transcript.ass"

    if input_video.exists():
        pytest.skip(f"Arquivo de teste já existe: {input_video}")

    shutil.copyfile(sample_video, input_video)
    save_json(
        {
            "source_audio": "cache/audio/000_pytest_phase3.wav",
            "language": "pt",
            "duration": 1.0,
            "segments": [
                {"start": 0.0, "end": 1.0, "text": "texto transcrito"},
            ],
        },
        transcript_output,
    )

    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

        logs = result.stdout + result.stderr
        assert result.returncode == 0, logs

        expected_order = [
            "Sistema iniciando",
            "Video AI Editor iniciado",
            "Vídeo encontrado: input/000_pytest_phase3.mp4",
            "Vídeo validado com sucesso",
            "Metadados carregados",
            "Áudio extraído: cache/audio/000_pytest_phase3.wav",
            "Validação Concluida",
            "Transcrição gerada: cache/transcripts/000_pytest_phase3_transcript.json",
            "SRT gerado: output/subtitles/000_pytest_phase3_transcript.srt",
            "ASS gerado: output/subtitles/000_pytest_phase3_transcript.ass",
            "Transcrição Concluida",
            "Fase 3 concluída com sucesso",
        ]

        positions = [logs.index(message) for message in expected_order]
        assert positions == sorted(positions)
        assert audio_output.exists()
        assert audio_output.stat().st_size > 0
        assert srt_output.exists()
        assert srt_output.stat().st_size > 0
        assert ass_output.exists()
        assert ass_output.stat().st_size > 0
    finally:
        input_video.unlink(missing_ok=True)
        audio_output.unlink(missing_ok=True)
        transcript_output.unlink(missing_ok=True)
        srt_output.unlink(missing_ok=True)
        ass_output.unlink(missing_ok=True)
