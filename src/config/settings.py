import os
from dotenv import load_dotenv


load_dotenv()


APP_NAME = "Video AI Editor"
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
AUDIO_CHANNELS = int(os.getenv("AUDIO_CHANNELS", "1"))
AUDIO_CODEC = os.getenv("AUDIO_CODEC", "pcm_s16le")
AUDIO_TEST_DURATION = int(os.getenv("AUDIO_TEST_DURATION", "60"))
AUDIO_FAST_TEST_MODE = os.getenv("AUDIO_FAST_TEST_MODE", "false").lower() == "true"
AUDIO_CREATE_CHUNKS = os.getenv("AUDIO_CREATE_CHUNKS", "true").lower() == "true"
AUDIO_CHUNK_DURATION = int(os.getenv("AUDIO_CHUNK_DURATION", "900"))
AUDIO_CHUNK_OVERLAP = int(os.getenv("AUDIO_CHUNK_OVERLAP", "2"))

WHISPER_PROFILE = os.getenv("WHISPER_PROFILE", "fast")

WHISPER_WORD_TIMESTAMPS = os.getenv("WHISPER_WORD_TIMESTAMPS", "false").lower() == "true"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "tiny")
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "pt")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
_WHISPER_CPU_THREADS = int(os.getenv("WHISPER_CPU_THREADS", "2"))
WHISPER_CPU_THREADS = (
    _WHISPER_CPU_THREADS
    if _WHISPER_CPU_THREADS > 0
    else max((os.cpu_count() or 2) - 1, 1)
)
WHISPER_NUM_WORKERS = int(os.getenv("WHISPER_NUM_WORKERS", "1"))
WHISPER_BEAM_SIZE = int(os.getenv("WHISPER_BEAM_SIZE", "0"))
WHISPER_BEST_OF = int(os.getenv("WHISPER_BEST_OF", "0"))
WHISPER_VAD_FILTER = os.getenv("WHISPER_VAD_FILTER", "true").lower() == "true"
WHISPER_CONDITION_ON_PREVIOUS_TEXT = (
    os.getenv("WHISPER_CONDITION_ON_PREVIOUS_TEXT", "false").lower() == "true"
)
TRANSCRIPTION_USE_CHUNKS = (
    os.getenv("TRANSCRIPTION_USE_CHUNKS", "true").lower() == "true"
)
TRANSCRIPTION_CHUNK_DURATION = int(os.getenv("TRANSCRIPTION_CHUNK_DURATION", "900"))
TRANSCRIPTION_CHUNK_OVERLAP = int(os.getenv("TRANSCRIPTION_CHUNK_OVERLAP", "2"))
TRANSCRIPTION_CHUNK_WORKERS = int(os.getenv("TRANSCRIPTION_CHUNK_WORKERS", "1"))
TRANSCRIPTION_CHUNKS_PARALLEL = (
    os.getenv("TRANSCRIPTION_CHUNKS_PARALLEL", "false").lower() == "true"
)

SHORT_MIN_DURATION = int(os.getenv("SHORT_MIN_DURATION", "15"))
SHORT_MAX_DURATION = int(os.getenv("SHORT_MAX_DURATION", "45"))
SHORTS_RENDER_PROFILE = os.getenv("SHORTS_RENDER_PROFILE", "fast")
SHORTS_RENDER_WORKERS = int(os.getenv("SHORTS_RENDER_WORKERS", "2"))
SHORTS_RENDER_PARALLEL = os.getenv("SHORTS_RENDER_PARALLEL", "true").lower() == "true"

LONG_VIDEO_MIN_DURATION = int(os.getenv("LONG_VIDEO_MIN_DURATION", str(20 * 60)))
LONG_VIDEO_MAX_DURATION = int(os.getenv("LONG_VIDEO_MAX_DURATION", str(30 * 60)))
LONG_RENDER_PROFILE = os.getenv("LONG_RENDER_PROFILE", "fast")
LONG_RENDER_PARALLEL = os.getenv("LONG_RENDER_PARALLEL", "true").lower() == "true"
LONG_RENDER_WORKERS = int(os.getenv("LONG_RENDER_WORKERS", "2"))
LONG_AUDIO_COPY = os.getenv("LONG_AUDIO_COPY", "false").lower() == "true"

MAX_SHORTS = int(os.getenv("MAX_SHORTS", "5"))
MAX_LONG_VIDEOS = int(os.getenv("MAX_LONG_VIDEOS", "1"))

VIDEO_OUTPUT_FORMAT = os.getenv("VIDEO_OUTPUT_FORMAT", "mp4")
VERTICAL_WIDTH = int(os.getenv("VERTICAL_WIDTH", "1080"))
VERTICAL_HEIGHT = int(os.getenv("VERTICAL_HEIGHT", "1920"))
VERTICAL_RENDER_PROFILE = os.getenv("VERTICAL_RENDER_PROFILE", "fast")
VERTICAL_RENDER_WORKERS = int(os.getenv("VERTICAL_RENDER_WORKERS", "2"))
VERTICAL_RENDER_PARALLEL = (
    os.getenv("VERTICAL_RENDER_PARALLEL", "true").lower() == "true"
)
VERTICAL_BLUR_ENABLED = os.getenv("VERTICAL_BLUR_ENABLED", "true").lower() == "true"
VERTICAL_FAST_MODE = os.getenv("VERTICAL_FAST_MODE", "false").lower() == "true"
VERTICAL_FAST_WIDTH = int(os.getenv("VERTICAL_FAST_WIDTH", "540"))
VERTICAL_FAST_HEIGHT = int(os.getenv("VERTICAL_FAST_HEIGHT", "960"))

HIGHLIGHT_MIN_SCORE = float(os.getenv("HIGHLIGHT_MIN_SCORE", "0.40"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
