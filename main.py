from pathlib import Path

from src.audio.extractor import extract_audio_from_video, format_project_path
from src.config.paths import CACHE_VIDEO_DIR, ensure_project_dirs
from src.config.settings import APP_ENV, APP_NAME
from src.utils.logger import get_logger
from src.video.converter import cut_video_segment
from src.video.metadata import format_duration, get_video_metadata
from src.video.reader import get_first_input_video
from src.video.validator import validate_video_file


logger = get_logger(__name__)


def run_phase_2_manual_test() -> None:
    ensure_project_dirs()

    logger.info("%s iniciado", APP_NAME)
    logger.info("Ambiente: %s", APP_ENV)

    video_path = get_first_input_video()
    logger.info("Vídeo encontrado: %s", format_project_path(Path(video_path)))

    validated_video = validate_video_file(video_path)
    logger.info("Vídeo validado com sucesso")

    metadata = get_video_metadata(validated_video)
    logger.info("Metadados carregados")
    logger.info("Duração: %s", format_duration(metadata["duration"]))
    logger.info("Resolução: %sx%s", metadata["width"], metadata["height"])
    logger.info("Codec de vídeo: %s", metadata["video_codec"])
    logger.info("Codec de áudio: %s", metadata["audio_codec"])

    audio_path = extract_audio_from_video(validated_video)
    logger.info("Áudio extraído: %s", format_project_path(audio_path))

    sample_clip_path = CACHE_VIDEO_DIR / "sample_10s.mp4"

    cut_video_segment(
        input_path=validated_video,
        output_path=sample_clip_path,
        start="00:00:00",
        end="00:00:10",
    )
    logger.info("Trecho de teste criado: %s", format_project_path(sample_clip_path))

    logger.info("Fase 2 concluída com sucesso")


def main() -> None:
    run_phase_2_manual_test()


if __name__ == "__main__":
    main()
