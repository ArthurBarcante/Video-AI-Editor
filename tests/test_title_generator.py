from pathlib import Path

from src.titles.title_generator import generate_titles
from src.titles.title_rules import (
    clean_title_text,
    generate_title_variants,
    score_title,
)
from src.utils.file_utils import load_json, save_json


def test_title_rules_generate_ctr_variants() -> None:
    assert clean_title_text("mano, não acredito nisso!") == "MANO, NÃO ACREDITO NISSO!"
    assert generate_title_variants("momento qualquer", style="intense") == [
        "ISSO FOI ABSURDO!",
        "EU NÃO ACREDITO QUE ISSO ACONTECEU",
        "MOMENTO QUALQUER",
    ]
    assert score_title("EU NÃO ACREDITO QUE ISSO ACONTECEU") == 0.8


def test_generate_titles_creates_suggestions_json(tmp_path: Path) -> None:
    edit_plan_path = tmp_path / "cache" / "edit_plans" / "edit_plan.json"
    context_path = tmp_path / "cache" / "context" / "context.json"
    emotions_path = tmp_path / "cache" / "emotions" / "emotions.json"
    output_path = tmp_path / "cache" / "titles" / "titles.json"
    save_json(
        {
            "source_video": "input/live.mp4",
            "shorts": [
                {
                    "id": "short_01",
                    "title": "MANO, NÃO ACREDITO NISSO!",
                    "style": "intense",
                }
            ],
            "long_videos": [
                {
                    "id": "video_01",
                    "title": "Melhores momentos da live",
                }
            ],
        },
        edit_plan_path,
    )
    save_json({"blocks": []}, context_path)
    save_json({"segments": []}, emotions_path)

    titles_path = generate_titles(
        edit_plan_path,
        output_path=output_path,
        context_path=context_path,
        emotions_path=emotions_path,
    )

    assert titles_path == output_path
    assert load_json(titles_path) == {
        "suggestions": [
            {
                "target_id": "short_01",
                "target_type": "short",
                "title": "EU NÃO ACREDITO QUE ISSO ACONTECEU",
                "score": 0.8,
                "reason": "gerado a partir do estilo intense",
            },
            {
                "target_id": "short_01",
                "target_type": "short",
                "title": "MANO, NÃO ACREDITO NISSO!",
                "score": 0.8,
                "reason": "gerado a partir do estilo intense",
            },
            {
                "target_id": "short_01",
                "target_type": "short",
                "title": "ISSO FOI ABSURDO!",
                "score": 0.7,
                "reason": "gerado a partir do estilo intense",
            },
            {
                "target_id": "video_01",
                "target_type": "long_video",
                "title": "OS MELHORES MOMENTOS DA LIVE",
                "score": 0.7,
                "reason": "título gerado para vídeo longo",
            },
            {
                "target_id": "video_01",
                "target_type": "long_video",
                "title": "MELHORES MOMENTOS COM A GALERA",
                "score": 0.7,
                "reason": "título gerado para vídeo longo",
            },
            {
                "target_id": "video_01",
                "target_type": "long_video",
                "title": "A LIVE MAIS CAÓTICA DO CANAL",
                "score": 0.6,
                "reason": "título gerado para vídeo longo",
            },
        ],
    }
