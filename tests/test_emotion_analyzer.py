from pathlib import Path

from src.emotion.emotion_analyzer import analyze_emotions
from src.emotion.emotion_rules import detect_emotion_from_text
from src.utils.file_utils import load_json, save_json


def test_detect_emotion_from_text_detects_core_emotions() -> None:
    assert detect_emotion_from_text("mano, não acredito nisso!") == (
        "surprise",
        0.33,
        ["surpresa: não acredito", "exclamação detectada"],
    )
    assert detect_emotion_from_text("que raiva, não dá!") == (
        "anger",
        0.5,
        ["raiva: não dá", "raiva: que raiva", "exclamação detectada"],
    )
    assert detect_emotion_from_text("boa, ganhei kkkk") == (
        "joy",
        0.75,
        ["alegria: boa", "alegria: ganhei", "alegria: kkkk"],
    )
    assert detect_emotion_from_text("vamos clipa isso!") == (
        "hype",
        0.62,
        [
            "empolgação: vamos",
            "empolgação: clipa",
            "exclamação detectada",
        ],
    )
    assert detect_emotion_from_text("conversa comum") == ("neutral", 0.0, [])


def test_analyze_emotions_generates_emotions_json(
    tmp_path: Path,
    sample_audio: Path,
) -> None:
    transcript_path = tmp_path / "cache" / "transcripts" / "live_transcript.json"
    output_path = tmp_path / "cache" / "emotions" / "emotions.json"
    save_json(
        {
            "source_audio": str(sample_audio),
            "language": "pt",
            "duration": 0.5,
            "segments": [
                {
                    "start": 0.0,
                    "end": 0.5,
                    "text": "mano, não acredito nisso!",
                }
            ],
        },
        transcript_path,
    )

    emotions_path = analyze_emotions(
        transcript_path=transcript_path,
        audio_path=sample_audio,
        output_path=output_path,
    )

    assert emotions_path == output_path
    analysis = load_json(emotions_path)
    assert analysis["source_transcript"] == str(transcript_path)
    assert analysis["source_audio"].endswith("sample.wav")
    assert analysis["segments"] == [
        {
            "start": 0.0,
            "end": 0.5,
            "text": "mano, não acredito nisso!",
            "emotion": "surprise",
            "emotion_score": 0.53,
            "audio_intensity": 1.0,
            "reasons": [
                "surpresa: não acredito",
                "exclamação detectada",
                "alta intensidade de áudio",
            ],
        }
    ]
