from pathlib import Path

from src.context.context_analyser import analyze_context
from src.context.topic_grouper import group_segments_into_blocks
from src.utils.file_utils import load_json, save_json


def test_analyze_context_generates_context_json(tmp_path: Path) -> None:
    transcript_path = tmp_path / "cache" / "transcripts" / "live_transcript.json"
    output_path = tmp_path / "cache" / "context" / "context.json"
    save_json(
        {
            "source_audio": "cache/audio/live.wav",
            "language": "pt",
            "duration": 190.0,
            "segments": [
                {
                    "start": 120.5,
                    "end": 140.0,
                    "text": "agora eu vou tentar passar desse boss",
                },
                {
                    "start": 142.0,
                    "end": 184.2,
                    "text": "morri antes mas agora tenho outra estratégia",
                },
            ],
        },
        transcript_path,
    )

    context_path = analyze_context(transcript_path, output_path=output_path)

    assert context_path == output_path
    assert load_json(context_path) == {
        "source_transcript": str(transcript_path),
        "blocks": [
            {
                "id": "context_001",
                "start": 120.5,
                "end": 184.2,
                "duration": 63.7,
                "text": (
                    "agora eu vou tentar passar desse boss "
                    "morri antes mas agora tenho outra estratégia"
                ),
                "keywords": ["boss", "morri", "estratégia"],
                "topic": "progressão de gameplay",
                "importance_score": 0.6,
                "reasons": [
                    "termos relevantes detectados",
                    "tópico relevante: progressão de gameplay",
                ],
            }
        ],
    }


def test_group_segments_into_blocks_splits_by_gap() -> None:
    blocks = group_segments_into_blocks(
        [
            {"start": 0.0, "end": 5.0, "text": "primeiro trecho"},
            {"start": 8.0, "end": 10.0, "text": "mesmo bloco"},
            {"start": 30.0, "end": 35.0, "text": "novo bloco"},
        ],
        max_gap=8.0,
    )

    assert blocks == [
        {
            "start": 0.0,
            "end": 10.0,
            "texts": ["primeiro trecho", "mesmo bloco"],
        },
        {
            "start": 30.0,
            "end": 35.0,
            "texts": ["novo bloco"],
        },
    ]
