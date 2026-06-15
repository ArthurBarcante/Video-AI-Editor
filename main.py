from pathlib import Path

from src.audio.extractor import extract_audio_from_video
from src.config.paths import ensure_project_dirs
from src.editing.long_video_builder import render_long_videos_from_edit_plan
from src.editing.shorts_builder import render_shorts_from_edit_plan
from src.config.settings import APP_ENV, APP_NAME
from src.highlights.detector import detect_highlights
from src.planning.edit_planner import generate_edit_plan
from src.rendering.verticalizer import verticalize_shorts
from src.subtitles.ass_generator import generate_ass
from src.subtitles.srt_generator import generate_srt
from src.transcription.whisper_transcriber import transcribe_audio
from src.utils.file_utils import format_project_path
from src.utils.logger import get_logger
from src.video.metadata import get_video_metadata
from src.video.reader import get_first_input_video
from src.video.validator import validate_video_file


logger = get_logger(__name__)


def main() -> None:
    ensure_project_dirs()

    logger.info("Sistema iniciando")
    logger.info("%s iniciado", APP_NAME)
    logger.info("Ambiente: %s", APP_ENV)

    video_path = get_first_input_video()
    logger.info("Vídeo encontrado: %s", format_project_path(Path(video_path)))

    validated_video = validate_video_file(video_path)
    logger.info("Vídeo validado com sucesso")

    metadata = get_video_metadata(validated_video)
    logger.info("Metadados carregados")
    logger.info("Duração: %.2f segundos", metadata["duration"])

    audio_path = extract_audio_from_video(validated_video)
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

    edit_plan_path = generate_edit_plan(
        source_video=validated_video,
        highlights_path=highlights_path,
    )
    logger.info("Edit plan pronto: %s", format_project_path(edit_plan_path))

    shorts_paths = render_shorts_from_edit_plan(edit_plan_path)
    for short_path in shorts_paths:
        logger.info("Short pronto: %s", format_project_path(short_path))

    vertical_paths = verticalize_shorts(shorts_paths)
    for vertical_path in vertical_paths:
        logger.info("Short vertical pronto: %s", format_project_path(vertical_path))

    long_video_paths = render_long_videos_from_edit_plan(edit_plan_path)
    for video_path in long_video_paths:
        logger.info("Vídeo longo pronto: %s", format_project_path(video_path))

    logger.info("Transcrição Concluida")
    logger.info("Fase 11 concluída com sucesso")


if __name__ == "__main__":
    main()
