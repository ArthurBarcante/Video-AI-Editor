from src.config.paths import (
    DEFAULT_AUDIO_PATH,
    DEFAULT_TRANSCRIPT_PATH,
    ensure_project_dirs,
)
from src.config.settings import APP_ENV, APP_NAME, WHISPER_MODEL
from src.utils.cache_utils import should_use_cache
from src.utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    ensure_project_dirs()

    logger.info("%s iniciado", APP_NAME)
    logger.info("Ambiente: %s", APP_ENV)
    logger.info("Modelo Whisper configurado: %s", WHISPER_MODEL)

    if should_use_cache(DEFAULT_AUDIO_PATH):
        logger.info("Cache de áudio encontrado: %s", DEFAULT_AUDIO_PATH)
    else:
        logger.info("Cache de áudio não encontrado. Extração será necessária.")

    if should_use_cache(DEFAULT_TRANSCRIPT_PATH):
        logger.info("Cache de transcrição encontrado: %s", DEFAULT_TRANSCRIPT_PATH)
    else:
        logger.info("Cache de transcrição não encontrado. Transcrição será necessária.")

    logger.info("Sistema de cache carregado com sucesso")


if __name__ == "__main__":
    main()
