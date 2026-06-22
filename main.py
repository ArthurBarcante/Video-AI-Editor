import argparse
import sys
from pathlib import Path

from src.audio.extractor import extract_audio_from_video
from src.config.paths import CACHE_AUDIO_DIR, ensure_project_dirs
from src.config.settings import APP_ENV, APP_NAME
from src.context.context_analyser import analyze_context
from src.editing.long_video_builder import render_long_videos_from_edit_plan
from src.editing.shorts_builder import render_shorts_from_edit_plan
from src.emotion.emotion_analyzer import analyze_emotions
from src.highlights.detector import detect_highlights
from src.learning.correction_memory import ensure_learning_files
from src.planning.edit_planner import generate_edit_plan
from src.publishing.publish_planner import generate_publish_plan
from src.rendering.verticalizer import verticalize_shorts
from src.subtitles.ass_generator import generate_ass
from src.subtitles.short_subtitle_generator import generate_short_ass_files
from src.subtitles.srt_generator import generate_srt
from src.thumbnails.thumbnail_generator import generate_thumbnails_from_edit_plan
from src.titles.title_generator import generate_titles
from src.transcription.whisper_transcriber import transcribe_audio
from src.utils.file_utils import format_project_path
from src.utils.logger import get_logger
from src.video.metadata import get_video_metadata
from src.video.reader import get_first_input_video
from src.video.validation_metadata import save_validation_metadata
from src.video.validator import validate_video_file


logger = get_logger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa o pipeline do Video AI Editor.",
    )
    parser.add_argument(
        "video_path",
        nargs="?",
        help="Caminho do vídeo bruto a processar.",
    )
    parser.add_argument(
        "--video",
        dest="video_option",
        help="Caminho do vídeo bruto a processar.",
    )

    args = parser.parse_args(argv)

    if args.video_path and args.video_option:
        parser.error("Use apenas um caminho: argumento posicional ou --video.")

    return args


def resolve_input_video(args: argparse.Namespace) -> Path:
    explicit_video = args.video_option or args.video_path

    if explicit_video:
        return Path(explicit_video)

    return get_first_input_video()


def main(argv: list[str] | None = None) -> None:
    ensure_project_dirs()
    args = parse_args(argv)

    logger.info("Sistema iniciando")
    logger.info("%s iniciado", APP_NAME)
    logger.info("Ambiente: %s", APP_ENV)
    ensure_learning_files()

    video_path = resolve_input_video(args)
    logger.info("Vídeo encontrado: %s", format_project_path(Path(video_path)))

    validated_video = validate_video_file(video_path)
    logger.info("Vídeo validado com sucesso")

    metadata = get_video_metadata(validated_video)
    logger.info("Metadados carregados")
    logger.info("Duração: %.2f segundos", metadata["duration"])
    validation_metadata_path = save_validation_metadata(validated_video, metadata)
    logger.info(
        "Metadata da validação salva em: %s",
        format_project_path(validation_metadata_path),
    )

    audio_path = extract_audio_from_video(
        video_path=validated_video,
        output_dir=CACHE_AUDIO_DIR,
    )
    logger.info("Áudio extraído: %s", format_project_path(audio_path))
    logger.info("Validação Concluida")

    transcript_path = transcribe_audio(audio_path)
    logger.info("Transcrição gerada: %s", format_project_path(transcript_path))

    srt_path = generate_srt(transcript_path)
    logger.info("SRT gerado: %s", format_project_path(srt_path))

    short_ass_path = generate_ass(
        transcript_path,
        mode="short",
    )
    logger.info("Legenda ASS para Shorts: %s", format_project_path(short_ass_path))

    long_ass_path = generate_ass(
        transcript_path,
        mode="long",
    )
    logger.info("Legenda ASS para vídeo longo: %s", format_project_path(long_ass_path))

    highlights_path = detect_highlights(
        transcript_path=transcript_path,
        audio_path=audio_path,
    )
    logger.info("Detecção de highlights concluída: %s", format_project_path(highlights_path))

    context_path = analyze_context(transcript_path)
    logger.info("Contexto pronto: %s", format_project_path(context_path))

    emotions_path = analyze_emotions(
        transcript_path=transcript_path,
        audio_path=audio_path,
    )
    logger.info("Emoções prontas: %s", format_project_path(emotions_path))

    edit_plan_path = generate_edit_plan(
        source_video=validated_video,
        highlights_path=highlights_path,
        context_path=context_path,
        emotions_path=emotions_path,
    )
    logger.info("Edit plan pronto: %s", format_project_path(edit_plan_path))

    short_ass_paths = generate_short_ass_files(
        transcript_path=transcript_path,
        edit_plan_path=edit_plan_path,
    )
    for short_ass_path in short_ass_paths:
        logger.info("Legenda ASS individual pronta: %s", format_project_path(short_ass_path))

    titles_path = generate_titles(
        edit_plan_path,
        context_path=context_path,
        emotions_path=emotions_path,
    )
    logger.info("Títulos prontos: %s", format_project_path(titles_path))

    thumbnail_paths = generate_thumbnails_from_edit_plan(edit_plan_path)
    for thumbnail_path in thumbnail_paths:
        logger.info("Thumbnail pronta: %s", format_project_path(thumbnail_path))

    shorts_paths = render_shorts_from_edit_plan(edit_plan_path)
    for short_path in shorts_paths:
        logger.info("Short pronto: %s", format_project_path(short_path))

    vertical_paths = verticalize_shorts(shorts_paths)
    for vertical_path in vertical_paths:
        logger.info("Short vertical pronto: %s", format_project_path(vertical_path))

    long_video_paths = render_long_videos_from_edit_plan(edit_plan_path)
    for video_path in long_video_paths:
        logger.info("Vídeo longo pronto: %s", format_project_path(video_path))

    publish_plan_path = generate_publish_plan(
        short_paths=shorts_paths,
        long_video_paths=long_video_paths,
    )
    logger.info("Plano de publicação pronto: %s", format_project_path(publish_plan_path))

    logger.info("Transcrição Concluida")
    logger.info("Fase 16 inicial concluída com sucesso")


if __name__ == "__main__":
    main(sys.argv[1:])
