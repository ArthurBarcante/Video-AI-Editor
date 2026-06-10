import logging
from logging import Logger

from src.config.settings import LOG_LEVEL


_LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%H:%M:%S"


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format=_LOG_FORMAT,
        datefmt=_DATE_FORMAT,
    )


def get_logger(name: str) -> Logger:
    setup_logging()
    return logging.getLogger(name)
