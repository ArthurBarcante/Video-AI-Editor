import os
from dotenv import load_dotenv


load_dotenv()


APP_NAME = "Video AI Editor"
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "tiny")
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "pt")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
_WHISPER_CPU_THREADS = int(os.getenv("WHISPER_CPU_THREADS", "0"))
WHISPER_CPU_THREADS = (
    _WHISPER_CPU_THREADS
    if _WHISPER_CPU_THREADS > 0
    else max((os.cpu_count() or 2) - 1, 1)
)
WHISPER_NUM_WORKERS = int(os.getenv("WHISPER_NUM_WORKERS", "2"))
WHISPER_BEAM_SIZE = int(os.getenv("WHISPER_BEAM_SIZE", "1"))
WHISPER_BEST_OF = int(os.getenv("WHISPER_BEST_OF", "1"))
WHISPER_VAD_FILTER = os.getenv("WHISPER_VAD_FILTER", "true").lower() == "true"
WHISPER_CONDITION_ON_PREVIOUS_TEXT = (
    os.getenv("WHISPER_CONDITION_ON_PREVIOUS_TEXT", "false").lower() == "true"
)

SHORT_MIN_DURATION = int(os.getenv("SHORT_MIN_DURATION", "15"))
SHORT_MAX_DURATION = int(os.getenv("SHORT_MAX_DURATION", "45"))

LONG_VIDEO_MIN_DURATION = int(os.getenv("LONG_VIDEO_MIN_DURATION", str(20 * 60)))
LONG_VIDEO_MAX_DURATION = int(os.getenv("LONG_VIDEO_MAX_DURATION", str(30 * 60)))

MAX_SHORTS = int(os.getenv("MAX_SHORTS", "5"))
MAX_LONG_VIDEOS = int(os.getenv("MAX_LONG_VIDEOS", "1"))

VIDEO_OUTPUT_FORMAT = os.getenv("VIDEO_OUTPUT_FORMAT", "mp4")
VERTICAL_WIDTH = int(os.getenv("VERTICAL_WIDTH", "1080"))
VERTICAL_HEIGHT = int(os.getenv("VERTICAL_HEIGHT", "1920"))

HIGHLIGHT_MIN_SCORE = float(os.getenv("HIGHLIGHT_MIN_SCORE", "0.40"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
