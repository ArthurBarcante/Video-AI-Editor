import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from src.config.paths import CACHE_AUDIO_DIR, CACHE_VIDEO_DIR, INPUT_DIR, ROOT_DIR


def test_python_main_runs_phase_2_in_expected_order(sample_video: Path) -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    input_video = INPUT_DIR / "000_pytest_phase2.mp4"
    audio_output = CACHE_AUDIO_DIR / "000_pytest_phase2.wav"
    sample_output = CACHE_VIDEO_DIR / "sample_10s.mp4"
    sample_existed_before = sample_output.exists()

    if input_video.exists():
        pytest.skip(f"Arquivo de teste já existe: {input_video}")

    shutil.copyfile(sample_video, input_video)

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
            "Video AI Editor iniciado",
            "Vídeo encontrado: input/000_pytest_phase2.mp4",
            "Vídeo validado com sucesso",
            "Metadados carregados",
            "Áudio extraído: cache/audio/000_pytest_phase2.wav",
            "Trecho de teste criado: cache/video/sample_10s.mp4",
            "Fase 2 concluída com sucesso",
        ]

        positions = [logs.index(message) for message in expected_order]
        assert positions == sorted(positions)
        assert audio_output.exists()
        assert audio_output.stat().st_size > 0
        assert sample_output.exists()
        assert sample_output.stat().st_size > 0
    finally:
        input_video.unlink(missing_ok=True)
        audio_output.unlink(missing_ok=True)
        if not sample_existed_before:
            sample_output.unlink(missing_ok=True)
