from pathlib import Path

from src.audio.extractor import extract_audio_from_video
from src.config.paths import ensure_project_dirs
from src.config.settings import APP_ENV, APP_NAME
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

    ass_path = generate_ass(transcript_path)
    logger.info("ASS gerado: %s", format_project_path(ass_path))

    logger.info("Transcrição Concluida")
    logger.info("Fase 3 concluída com sucesso")


if __name__ == "__main__":
    main()
