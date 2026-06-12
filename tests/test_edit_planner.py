from pathlib import Path

from src.config.paths import INPUT_DIR
from src.planning.edit_planner import generate_edit_plan
from src.utils.file_utils import load_json, save_json


def test_generate_edit_plan_creates_expected_structure(tmp_path: Path) -> None:
    highlights_path = tmp_path / "cache" / "highlights" / "highlights.json"
    output_path = tmp_path / "cache" / "edit_plans" / "edit_plan.json"
    source_video = INPUT_DIR / "live_bruta.mp4"

    save_json(
        [
            {
                "start": 118.4,
                "end": 124.2,
                "text": "mano, não acredito nisso!",
                "score": 0.82,
                "reasons": [
                    "palavra-chave: mano",
                    "exclamação detectada",
                    "alta intensidade de áudio",
                ],
            },
            {
                "start": 200.0,
                "end": 206.0,
                "text": "momento menor",
                "score": 0.5,
                "reasons": ["intensidade média de áudio"],
            },
            {
                "start": 300.0,
                "end": 360.0,
                "text": "caraca, olha esse momento longo!",
                "score": 0.75,
                "reasons": [
                    "palavra-chave: caraca",
                    "exclamação detectada",
                ],
            },
        ],
        highlights_path,
    )

    edit_plan_path = generate_edit_plan(
        source_video=source_video,
        highlights_path=highlights_path,
        output_path=output_path,
    )

    assert edit_plan_path == output_path
    assert load_json(output_path) == {
        "source_video": "input/live_bruta.mp4",
        "shorts": [
            {
                "id": "short_01",
                "start": 118.4,
                "end": 133.4,
                "duration": 15.0,
                "score": 1.0,
                "title": "MANO, NÃO ACREDITO NISSO!",
                "reason": (
                    "palavra-chave: mano, exclamação detectada, "
                    "alta intensidade de áudio"
                ),
                "style": "intense",
                "actions": [
                    {
                        "type": "zoom",
                        "start": 118.4,
                        "end": 120.9,
                        "time": None,
                        "intensity": 1.2,
                        "target": "center",
                        "name": None,
                        "style": None,
                    },
                    {
                        "type": "subtitle_emphasis",
                        "start": 118.4,
                        "end": 124.2,
                        "time": None,
                        "intensity": None,
                        "target": None,
                        "name": None,
                        "style": "impact",
                    },
                ],
            },
            {
                "id": "short_02",
                "start": 300.0,
                "end": 345.0,
                "duration": 45.0,
                "score": 0.99,
                "title": "CARACA, OLHA ESSE MOMENTO LONGO!",
                "reason": "palavra-chave: caraca, exclamação detectada",
                "style": "intense",
                "actions": [
                    {
                        "type": "subtitle_emphasis",
                        "start": 300.0,
                        "end": 360.0,
                        "time": None,
                        "intensity": None,
                        "target": None,
                        "name": None,
                        "style": "impact",
                    }
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
                        "start": 110.4,
                        "end": 132.2,
                        "duration": 21.8,
                        "score": 0.82,
                        "reason": (
                            "palavra-chave: mano, exclamação detectada, "
                            "alta intensidade de áudio"
                        ),
                    },
                    {
                        "start": 192.0,
                        "end": 214.0,
                        "duration": 22.0,
                        "score": 0.5,
                        "reason": "intensidade média de áudio",
                    },
                    {
                        "start": 292.0,
                        "end": 368.0,
                        "duration": 76.0,
                        "score": 0.75,
                        "reason": "palavra-chave: caraca, exclamação detectada",
                    }
                ],
                "actions": [],
            }
        ],
    }
