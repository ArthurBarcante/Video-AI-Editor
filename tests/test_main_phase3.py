import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from src.config.paths import (
    CACHE_AUDIO_DIR,
    CACHE_EDIT_PLANS_DIR,
    CACHE_HIGHLIGHTS_DIR,
    CACHE_TRANSCRIPTS_DIR,
    INPUT_DIR,
    OUTPUT_LONG_DIR,
    OUTPUT_SHORTS_DIR,
    OUTPUT_SUBTITLES_DIR,
    OUTPUT_VERTICAL_DIR,
    ROOT_DIR,
)
from src.utils.file_utils import load_json, save_json


def test_python_main_runs_through_highlights_in_expected_order(sample_video: Path) -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    input_video = INPUT_DIR / "000_pytest_phase3.mp4"
    audio_output = CACHE_AUDIO_DIR / "000_pytest_phase3.wav"
    transcript_output = CACHE_TRANSCRIPTS_DIR / "000_pytest_phase3_transcript.json"
    highlights_output = CACHE_HIGHLIGHTS_DIR / "highlights.json"
    edit_plan_output = CACHE_EDIT_PLANS_DIR / "edit_plan.json"
    short_output = OUTPUT_SHORTS_DIR / "short_01.mp4"
    vertical_output = OUTPUT_VERTICAL_DIR / "short_01_vertical.mp4"
    long_video_output = OUTPUT_LONG_DIR / "video_01.mp4"
    srt_output = OUTPUT_SUBTITLES_DIR / "000_pytest_phase3_transcript.srt"
    short_ass_output = OUTPUT_SUBTITLES_DIR / "000_pytest_phase3_transcript_short.ass"
    long_ass_output = OUTPUT_SUBTITLES_DIR / "000_pytest_phase3_transcript_long.ass"

    if input_video.exists():
        pytest.skip(f"Arquivo de teste já existe: {input_video}")

    shutil.copyfile(sample_video, input_video)
    save_json(
        {
            "source_audio": "cache/audio/000_pytest_phase3.wav",
            "language": "pt",
            "duration": 1.0,
            "segments": [
                {"start": 0.0, "end": 3.0, "text": "mano, não acredito nisso!"},
            ],
        },
        transcript_output,
    )
    previous_highlights = (
        highlights_output.read_text(encoding="utf-8") if highlights_output.exists() else None
    )
    previous_edit_plan = (
        edit_plan_output.read_text(encoding="utf-8") if edit_plan_output.exists() else None
    )
    previous_short = short_output.read_bytes() if short_output.exists() else None
    previous_vertical = vertical_output.read_bytes() if vertical_output.exists() else None
    previous_long_video = (
        long_video_output.read_bytes() if long_video_output.exists() else None
    )
    highlights_output.unlink(missing_ok=True)
    edit_plan_output.unlink(missing_ok=True)
    short_output.unlink(missing_ok=True)
    vertical_output.unlink(missing_ok=True)
    long_video_output.unlink(missing_ok=True)
    short_ass_output.unlink(missing_ok=True)
    long_ass_output.unlink(missing_ok=True)

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
            (
                "Legenda ASS para Shorts: "
                "output/subtitles/000_pytest_phase3_transcript_short.ass"
            ),
            (
                "Legenda ASS para vídeo longo: "
                "output/subtitles/000_pytest_phase3_transcript_long.ass"
            ),
            "Highlights gerados: 1",
            "Arquivo salvo em: cache/highlights/highlights.json",
            "Detecção de highlights concluída: cache/highlights/highlights.json",
            "Edit plan gerado: cache/edit_plans/edit_plan.json",
            "Edit plan pronto: cache/edit_plans/edit_plan.json",
            "Short exportado: output/shorts/short_01.mp4",
            "Shorts renderizados: 1",
            "Short pronto: output/shorts/short_01.mp4",
            "Vídeo vertical gerado: output/vertical/short_01_vertical.mp4",
            "Shorts verticalizados: 1",
            "Short vertical pronto: output/vertical/short_01_vertical.mp4",
            "Vídeo longo exportado: output/long/video_01.mp4",
            "Vídeos longos renderizados: 1",
            "Vídeo longo pronto: output/long/video_01.mp4",
            "Transcrição Concluida",
            "Fase 11 concluída com sucesso",
        ]

        positions = [logs.index(message) for message in expected_order]
        assert positions == sorted(positions)
        assert audio_output.exists()
        assert audio_output.stat().st_size > 0
        assert srt_output.exists()
        assert srt_output.stat().st_size > 0
        assert short_ass_output.exists()
        assert short_ass_output.stat().st_size > 0
        assert long_ass_output.exists()
        assert long_ass_output.stat().st_size > 0
        assert short_output.exists()
        assert short_output.stat().st_size > 0
        assert vertical_output.exists()
        assert vertical_output.stat().st_size > 0
        assert long_video_output.exists()
        assert long_video_output.stat().st_size > 0
        assert load_json(highlights_output) == [
            {
                "start": 0.0,
                "end": 3.0,
                "text": "mano, não acredito nisso!",
                "score": 0.83,
                "reasons": [
                    "palavra-chave: mano",
                    "palavra-chave: não acredito",
                    "exclamação detectada",
                    "fala curta com potencial de corte",
                    "alta intensidade de áudio",
                ],
            }
        ]
        assert load_json(edit_plan_output) == {
            "source_video": "input/000_pytest_phase3.mp4",
            "shorts": [
                {
                    "id": "short_01",
                    "start": 0.0,
                    "end": 15.0,
                    "duration": 15.0,
                    "score": 1.0,
                    "title": "MANO, NÃO ACREDITO NISSO!",
                    "reason": (
                        "palavra-chave: mano, palavra-chave: não acredito, "
                        "exclamação detectada, fala curta com potencial de corte, "
                        "alta intensidade de áudio"
                    ),
                    "style": "intense",
                    "actions": [
                        {
                            "type": "zoom",
                            "intensity": 1.25,
                            "target": "center",
                            "reason": "zoom por alta intensidade",
                        },
                        {
                            "type": "sfx",
                            "time": 0.0,
                            "volume": 0.35,
                            "reason": "sfx por alta intensidade",
                            "name": "impact",
                        },
                    ],
                }
            ],
            "long_videos": [
                {
                    "id": "video_01",
                    "title": "Melhores momentos da live",
                    "duration_target": 1200,
                    "theme": "compilado curto de melhores momentos",
                    "segments": [
                        {
                            "start": 0.0,
                            "end": 11.0,
                            "duration": 11.0,
                            "score": 0.83,
                            "reason": (
                                "palavra-chave: mano, palavra-chave: não acredito, "
                                "exclamação detectada, fala curta com potencial de corte, "
                                "alta intensidade de áudio"
                            ),
                        }
                    ],
                    "actions": [],
                }
            ],
        }
    finally:
        input_video.unlink(missing_ok=True)
        audio_output.unlink(missing_ok=True)
        transcript_output.unlink(missing_ok=True)
        srt_output.unlink(missing_ok=True)
        short_ass_output.unlink(missing_ok=True)
        long_ass_output.unlink(missing_ok=True)
        if previous_highlights is None:
            highlights_output.unlink(missing_ok=True)
        else:
            highlights_output.write_text(previous_highlights, encoding="utf-8")
        if previous_edit_plan is None:
            edit_plan_output.unlink(missing_ok=True)
        else:
            edit_plan_output.write_text(previous_edit_plan, encoding="utf-8")
        if previous_short is None:
            short_output.unlink(missing_ok=True)
        else:
            short_output.parent.mkdir(parents=True, exist_ok=True)
            short_output.write_bytes(previous_short)
        if previous_vertical is None:
            vertical_output.unlink(missing_ok=True)
        else:
            vertical_output.parent.mkdir(parents=True, exist_ok=True)
            vertical_output.write_bytes(previous_vertical)
        if previous_long_video is None:
            long_video_output.unlink(missing_ok=True)
        else:
            long_video_output.parent.mkdir(parents=True, exist_ok=True)
            long_video_output.write_bytes(previous_long_video)
