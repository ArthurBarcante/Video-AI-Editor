from pathlib import Path
from typing import Any

from src.config.paths import CACHE_TRANSCRIPTS_DIR
from src.config.settings import (
    WHISPER_BEAM_SIZE,
    WHISPER_BEST_OF,
    WHISPER_COMPUTE_TYPE,
    WHISPER_CONDITION_ON_PREVIOUS_TEXT,
    WHISPER_CPU_THREADS,
    WHISPER_DEVICE,
    WHISPER_LANGUAGE,
    WHISPER_MODEL,
    WHISPER_NUM_WORKERS,
    WHISPER_VAD_FILTER,
)
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.transcription.transcript_schema import Transcript, TranscriptSegment
from src.utils.file_utils import format_project_path, save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


class TranscriptionError(RuntimeError):
    pass


def get_whisper_model_class() -> Any:
    try:
        from faster_whisper import WhisperModel
    except ImportError as error:
        raise TranscriptionError(
            "faster-whisper não está instalado. Instale as dependências do projeto."
        ) from error

    return WhisperModel


def validate_audio_file(audio_path: Path) -> None:
    if not audio_path.exists():
        raise FileNotFoundError(f"Áudio não encontrado: {audio_path}")

    if not audio_path.is_file():
        raise ValueError(f"O caminho do áudio não é um arquivo: {audio_path}")

    if audio_path.suffix.lower() != ".wav":
        raise ValueError(f"O arquivo de áudio não é .wav: {audio_path}")

    if audio_path.stat().st_size == 0:
        raise ValueError(f"O arquivo de áudio está vazio: {audio_path}")


def transcribe_audio(
    audio_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
) -> Path:
    audio_path = Path(audio_path)
    validate_audio_file(audio_path)

    if output_path is None:
        output_path = CACHE_TRANSCRIPTS_DIR / f"{audio_path.stem}_transcript.json"

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)

    if output_path.exists() and not force:
        logger.info("Transcrição já existe em cache: %s", format_project_path(output_path))
        return output_path

    logger.info("Carregando modelo Whisper: %s", WHISPER_MODEL)

    whisper_model_class = get_whisper_model_class()
    model = whisper_model_class(
        WHISPER_MODEL,
        device=WHISPER_DEVICE,
        compute_type=WHISPER_COMPUTE_TYPE,
        cpu_threads=WHISPER_CPU_THREADS,
        num_workers=WHISPER_NUM_WORKERS,
    )

    logger.info(
        "Transcrevendo áudio: %s com beam_size=%s, vad_filter=%s",
        format_project_path(audio_path),
        WHISPER_BEAM_SIZE,
        WHISPER_VAD_FILTER,
    )

    segments, info = model.transcribe(
        str(audio_path),
        language=WHISPER_LANGUAGE,
        vad_filter=WHISPER_VAD_FILTER,
        beam_size=WHISPER_BEAM_SIZE,
        best_of=WHISPER_BEST_OF,
        condition_on_previous_text=WHISPER_CONDITION_ON_PREVIOUS_TEXT,
    )

    transcript_segments = []
    for segment in segments:
        text = str(segment.text).strip()
        if not text:
            continue

        transcript_segments.append(
            TranscriptSegment(
                start=float(segment.start),
                end=float(segment.end),
                text=text,
            )
        )

    transcript = Transcript(
        source_audio=format_project_path(audio_path),
        language=getattr(info, "language", WHISPER_LANGUAGE),
        duration=getattr(info, "duration", None),
        segments=transcript_segments,
    )

    save_json(
        transcript.model_dump(),
        output_path,
    )

    logger.info("Transcrição salva em: %s", format_project_path(output_path))

    return output_path
