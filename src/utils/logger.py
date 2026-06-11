import logging
from logging import Logger

from src.config.settings import LOG_LEVEL

_LOG_FORMAT = "[%(levelname)s] %(message)s"


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format=_LOG_FORMAT,
    )


def get_logger(name: str) -> Logger:
    setup_logging()
    return logging.getLogger(name)
