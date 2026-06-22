import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from src.audio.cache_signature import build_video_cache_signature
from src.config.paths import (
    CACHE_AUDIO_DIR,
    CACHE_CONTEXT_DIR,
    CACHE_EMOTIONS_DIR,
    CACHE_EDIT_PLANS_DIR,
    CACHE_HIGHLIGHTS_DIR,
    CACHE_METADATA_DIR,
    CACHE_PUBLISH_DIR,
    CACHE_TITLES_DIR,
    CACHE_TRANSCRIPTS_DIR,
    INPUT_DIR,
    OUTPUT_LONG_DIR,
    OUTPUT_SHORTS_DIR,
    OUTPUT_SUBTITLES_DIR,
    OUTPUT_THUMBNAILS_DIR,
    OUTPUT_VERTICAL_DIR,
    ROOT_DIR,
)
from src.utils.file_utils import load_json, save_json


def test_python_main_runs_through_highlights_in_expected_order(sample_video: Path) -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    input_video = INPUT_DIR / "000_pytest_phase3.mp4"
    validation_metadata_output = (
        CACHE_METADATA_DIR / "000_pytest_phase3_validation_metadata.json"
    )
    context_output = CACHE_CONTEXT_DIR / "context.json"
    emotions_output = CACHE_EMOTIONS_DIR / "emotions.json"
    highlights_output = CACHE_HIGHLIGHTS_DIR / "highlights.json"
    edit_plan_output = CACHE_EDIT_PLANS_DIR / "edit_plan.json"
    titles_output = CACHE_TITLES_DIR / "titles.json"
    publish_plan_output = CACHE_PUBLISH_DIR / "publish_plan.json"
    short_output = OUTPUT_SHORTS_DIR / "short_01.mp4"
    short_thumbnail_output = OUTPUT_THUMBNAILS_DIR / "short_01.jpg"
    short_thumbnail_frame = OUTPUT_THUMBNAILS_DIR / "frames" / "short_01_frame.jpg"
    long_thumbnail_output = OUTPUT_THUMBNAILS_DIR / "video_01.jpg"
    long_thumbnail_frame = OUTPUT_THUMBNAILS_DIR / "frames" / "video_01_frame.jpg"
    vertical_output = OUTPUT_VERTICAL_DIR / "short_01_vertical.mp4"
    long_video_output = OUTPUT_LONG_DIR / "video_01.mp4"

    if input_video.exists():
        pytest.skip(f"Arquivo de teste já existe: {input_video}")

    shutil.copyfile(sample_video, input_video)
    audio_signature = build_video_cache_signature(input_video)
    audio_stem = f"000_pytest_phase3_{audio_signature}"
    audio_output = CACHE_AUDIO_DIR / f"{audio_stem}.wav"
    audio_metadata_output = CACHE_AUDIO_DIR / f"{audio_stem}_audio_metadata.json"
    audio_chunks_dir = CACHE_AUDIO_DIR / "chunks" / audio_stem
    transcript_output = CACHE_TRANSCRIPTS_DIR / f"{audio_stem}_transcript.json"
    srt_output = OUTPUT_SUBTITLES_DIR / f"{audio_stem}_transcript.srt"
    short_ass_output = OUTPUT_SUBTITLES_DIR / f"{audio_stem}_transcript_short.ass"
    long_ass_output = OUTPUT_SUBTITLES_DIR / f"{audio_stem}_transcript_long.ass"
    save_json(
        {
            "source_audio": f"cache/audio/{audio_stem}.wav",
            "language": "pt",
            "duration": 1.0,
            "segments": [
                {"start": 0.0, "end": 3.0, "text": "mano, não acredito nisso!"},
            ],
            "metadata": {
                "execution_time_seconds": 1.0,
                "audio_duration_seconds": 3.0,
                "realtime_speed": 3.0,
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
        transcript_output,
    )
    previous_highlights = (
        highlights_output.read_text(encoding="utf-8") if highlights_output.exists() else None
    )
    previous_edit_plan = (
        edit_plan_output.read_text(encoding="utf-8") if edit_plan_output.exists() else None
    )
    previous_titles = (
        titles_output.read_text(encoding="utf-8") if titles_output.exists() else None
    )
    previous_publish_plan = (
        publish_plan_output.read_text(encoding="utf-8")
        if publish_plan_output.exists()
        else None
    )
    previous_context = (
        context_output.read_text(encoding="utf-8") if context_output.exists() else None
    )
    previous_emotions = (
        emotions_output.read_text(encoding="utf-8") if emotions_output.exists() else None
    )
    previous_short = short_output.read_bytes() if short_output.exists() else None
    previous_short_thumbnail = (
        short_thumbnail_output.read_bytes()
        if short_thumbnail_output.exists()
        else None
    )
    previous_short_thumbnail_frame = (
        short_thumbnail_frame.read_bytes()
        if short_thumbnail_frame.exists()
        else None
    )
    previous_long_thumbnail = (
        long_thumbnail_output.read_bytes()
        if long_thumbnail_output.exists()
        else None
    )
    previous_long_thumbnail_frame = (
        long_thumbnail_frame.read_bytes()
        if long_thumbnail_frame.exists()
        else None
    )
    previous_vertical = vertical_output.read_bytes() if vertical_output.exists() else None
    previous_long_video = (
        long_video_output.read_bytes() if long_video_output.exists() else None
    )
    highlights_output.unlink(missing_ok=True)
    context_output.unlink(missing_ok=True)
    emotions_output.unlink(missing_ok=True)
    edit_plan_output.unlink(missing_ok=True)
    titles_output.unlink(missing_ok=True)
    publish_plan_output.unlink(missing_ok=True)
    short_output.unlink(missing_ok=True)
    short_thumbnail_output.unlink(missing_ok=True)
    short_thumbnail_frame.unlink(missing_ok=True)
    long_thumbnail_output.unlink(missing_ok=True)
    long_thumbnail_frame.unlink(missing_ok=True)
    vertical_output.unlink(missing_ok=True)
    long_video_output.unlink(missing_ok=True)
    validation_metadata_output.unlink(missing_ok=True)
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
            (
                "Metadata da validação salva em: "
                "cache/metadata/000_pytest_phase3_validation_metadata.json"
            ),
            f"Áudio extraído: cache/audio/{audio_stem}.wav",
            "Validação Concluida",
            f"Transcrição gerada: cache/transcripts/{audio_stem}_transcript.json",
            f"SRT gerado: output/subtitles/{audio_stem}_transcript.srt",
            (
                "Legenda ASS para Shorts: "
                f"output/subtitles/{audio_stem}_transcript_short.ass"
            ),
            (
                "Legenda ASS para vídeo longo: "
                f"output/subtitles/{audio_stem}_transcript_long.ass"
            ),
            "Highlights gerados: 1",
            "Arquivo salvo em: cache/highlights/highlights.json",
            "Detecção de highlights concluída: cache/highlights/highlights.json",
            "Blocos de contexto gerados: 1",
            "Contexto salvo em: cache/context/context.json",
            "Contexto pronto: cache/context/context.json",
            "Análise emocional salva em: cache/emotions/emotions.json",
            "Emoções prontas: cache/emotions/emotions.json",
            "Edit plan gerado: cache/edit_plans/edit_plan.json",
            "Edit plan pronto: cache/edit_plans/edit_plan.json",
            "Sugestões de títulos geradas: 3",
            "Títulos salvos em: cache/titles/titles.json",
            "Títulos prontos: cache/titles/titles.json",
            "Thumbnail gerada: output/thumbnails/short_01.jpg",
            "Thumbnail pronta: output/thumbnails/short_01.jpg",
            "Short exportado: output/shorts/short_01.mp4",
            "Shorts renderizados: 1",
            "Short pronto: output/shorts/short_01.mp4",
            "Vídeo vertical gerado: output/vertical/short_01_vertical.mp4",
            "Shorts verticalizados: 1",
            "Short vertical pronto: output/vertical/short_01_vertical.mp4",
            "Vídeos longos renderizados: 0",
            "Publish plan gerado: cache/publishing/publish_plan.json",
            "Plano de publicação pronto: cache/publishing/publish_plan.json",
            "Transcrição Concluida",
            "Fase 16 inicial concluída com sucesso",
        ]

        positions = [logs.index(message) for message in expected_order]
        assert positions == sorted(positions)
        assert audio_output.exists()
        assert audio_output.stat().st_size > 0
        assert audio_metadata_output.exists()
        assert audio_metadata_output.stat().st_size > 0
        assert audio_chunks_dir.exists()
        assert validation_metadata_output.exists()
        assert validation_metadata_output.stat().st_size > 0
        assert srt_output.exists()
        assert srt_output.stat().st_size > 0
        assert short_ass_output.exists()
        assert short_ass_output.stat().st_size > 0
        assert long_ass_output.exists()
        assert long_ass_output.stat().st_size > 0
        assert context_output.exists()
        assert context_output.stat().st_size > 0
        assert emotions_output.exists()
        assert emotions_output.stat().st_size > 0
        assert titles_output.exists()
        assert titles_output.stat().st_size > 0
        assert short_thumbnail_output.exists()
        assert short_thumbnail_output.stat().st_size > 0
        assert short_thumbnail_frame.exists()
        assert short_thumbnail_frame.stat().st_size > 0
        assert not long_thumbnail_output.exists()
        assert not long_thumbnail_frame.exists()
        assert short_output.exists()
        assert short_output.stat().st_size > 0
        assert vertical_output.exists()
        assert vertical_output.stat().st_size > 0
        assert not long_video_output.exists()
        assert publish_plan_output.exists()
        assert publish_plan_output.stat().st_size > 0
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
        validation_metadata = load_json(validation_metadata_output)
        assert validation_metadata["file_name"] == "000_pytest_phase3.mp4"
        assert validation_metadata["source_path"] == "input/000_pytest_phase3.mp4"
        assert validation_metadata["duration"] > 0
        assert validation_metadata["width"] == 160
        assert validation_metadata["height"] == 120
        assert validation_metadata["fps"] == 25.0
        assert validation_metadata["codec"] == "h264"
        assert validation_metadata["audio_codec"] == "aac"
        assert validation_metadata["file_size_bytes"] > 0
        assert validation_metadata["validated_at"]
        audio_metadata = load_json(audio_metadata_output)
        assert audio_metadata["cache_signature"] == audio_signature
        assert audio_metadata["audio_path"] == f"cache/audio/{audio_stem}.wav"
        assert audio_metadata["chunk_count"] >= 1
        assert audio_metadata["chunks_metadata_path"]
        assert load_json(context_output) == {
            "source_transcript": (
                f"cache/transcripts/{audio_stem}_transcript.json"
            ),
            "blocks": [
                {
                    "id": "context_001",
                    "start": 0.0,
                    "end": 3.0,
                    "duration": 3.0,
                    "text": "mano, não acredito nisso!",
                    "keywords": [],
                    "topic": "conversa geral",
                    "importance_score": 0.0,
                    "reasons": [],
                }
            ],
        }
        assert load_json(emotions_output) == {
            "source_transcript": (
                f"cache/transcripts/{audio_stem}_transcript.json"
            ),
            "source_audio": f"cache/audio/{audio_stem}.wav",
            "segments": [
                {
                    "start": 0.0,
                    "end": 3.0,
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
            ],
        }
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
            "long_videos": [],
        }
        assert load_json(titles_output)["suggestions"][:2] == [
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
        ]
        publish_items = load_json(publish_plan_output)["items"]
        assert {
            "platform": "youtube_shorts",
            "video_path": "output/shorts/short_01.mp4",
            "title": "SHORT 01",
            "description": "Short gerado automaticamente pelo Video AI Editor.",
            "tags": ["shorts", "live", "gameplay"],
            "scheduled_at": None,
            "privacy_status": "private",
            "status": "pending",
        } in publish_items
        assert not any(item["platform"] == "youtube" for item in publish_items)
    finally:
        input_video.unlink(missing_ok=True)
        audio_output.unlink(missing_ok=True)
        audio_metadata_output.unlink(missing_ok=True)
        shutil.rmtree(audio_chunks_dir, ignore_errors=True)
        validation_metadata_output.unlink(missing_ok=True)
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
        if previous_titles is None:
            titles_output.unlink(missing_ok=True)
        else:
            titles_output.write_text(previous_titles, encoding="utf-8")
        if previous_publish_plan is None:
            publish_plan_output.unlink(missing_ok=True)
        else:
            publish_plan_output.write_text(previous_publish_plan, encoding="utf-8")
        if previous_context is None:
            context_output.unlink(missing_ok=True)
        else:
            context_output.write_text(previous_context, encoding="utf-8")
        if previous_emotions is None:
            emotions_output.unlink(missing_ok=True)
        else:
            emotions_output.write_text(previous_emotions, encoding="utf-8")
        if previous_short is None:
            short_output.unlink(missing_ok=True)
        else:
            short_output.parent.mkdir(parents=True, exist_ok=True)
            short_output.write_bytes(previous_short)
        if previous_short_thumbnail is None:
            short_thumbnail_output.unlink(missing_ok=True)
        else:
            short_thumbnail_output.parent.mkdir(parents=True, exist_ok=True)
            short_thumbnail_output.write_bytes(previous_short_thumbnail)
        if previous_short_thumbnail_frame is None:
            short_thumbnail_frame.unlink(missing_ok=True)
        else:
            short_thumbnail_frame.parent.mkdir(parents=True, exist_ok=True)
            short_thumbnail_frame.write_bytes(previous_short_thumbnail_frame)
        if previous_long_thumbnail is None:
            long_thumbnail_output.unlink(missing_ok=True)
        else:
            long_thumbnail_output.parent.mkdir(parents=True, exist_ok=True)
            long_thumbnail_output.write_bytes(previous_long_thumbnail)
        if previous_long_thumbnail_frame is None:
            long_thumbnail_frame.unlink(missing_ok=True)
        else:
            long_thumbnail_frame.parent.mkdir(parents=True, exist_ok=True)
            long_thumbnail_frame.write_bytes(previous_long_thumbnail_frame)
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
