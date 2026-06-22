import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from src.config.paths import CACHE_TRANSCRIPTS_DIR, CACHE_TRANSCRIPTION_CHUNKS_DIR
from src.config.settings import (
    TRANSCRIPTION_CHUNK_DURATION,
    TRANSCRIPTION_CHUNK_OVERLAP,
    TRANSCRIPTION_CHUNK_WORKERS,
    TRANSCRIPTION_CHUNKS_PARALLEL,
    TRANSCRIPTION_USE_CHUNKS,
    WHISPER_BEAM_SIZE,
    WHISPER_BEST_OF,
    WHISPER_COMPUTE_TYPE,
    WHISPER_CONDITION_ON_PREVIOUS_TEXT,
    WHISPER_CPU_THREADS,
    WHISPER_DEVICE,
    WHISPER_LANGUAGE,
    WHISPER_MODEL,
    WHISPER_NUM_WORKERS,
    WHISPER_PROFILE,
    WHISPER_VAD_FILTER,
    WHISPER_WORD_TIMESTAMPS,
)
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.transcription.chunk_merger import merge_chunk_segments
from src.transcription.chunk_transcriber import transcribe_chunk
from src.transcription.chunking import build_chunk_ranges, create_audio_chunk
from src.transcription.text_cleaner import clean_transcript_text
from src.transcription.transcript_schema import (
    Transcript,
    TranscriptMetadata,
    TranscriptSegment,
)
from src.transcription.transcription_profiles import get_transcription_profile
from src.video.metadata import get_video_metadata
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


def get_transcription_config() -> dict:
    profile = get_transcription_profile(WHISPER_PROFILE)

    return {
        "profile": profile,
        "beam_size": WHISPER_BEAM_SIZE or profile["beam_size"],
        "best_of": WHISPER_BEST_OF or profile["best_of"],
        "word_timestamps": WHISPER_WORD_TIMESTAMPS,
        "condition_on_previous_text": WHISPER_CONDITION_ON_PREVIOUS_TEXT,
        "vad_filter": WHISPER_VAD_FILTER,
        "vad_parameters": profile.get("vad_parameters"),
    }


def create_whisper_model() -> Any:
    logger.info("Carregando modelo Whisper: %s", WHISPER_MODEL)

    whisper_model_class = get_whisper_model_class()
    return whisper_model_class(
        WHISPER_MODEL,
        device=WHISPER_DEVICE,
        compute_type=WHISPER_COMPUTE_TYPE,
        cpu_threads=WHISPER_CPU_THREADS,
        num_workers=WHISPER_NUM_WORKERS,
    )


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

    if TRANSCRIPTION_USE_CHUNKS:
        return transcribe_audio_by_chunks(
            audio_path=audio_path,
            output_path=output_path,
            force=force,
        )

    return transcribe_audio_full(
        audio_path=audio_path,
        output_path=output_path,
    )


def transcribe_audio_full(
    audio_path: str | Path,
    output_path: str | Path,
) -> Path:
    audio_path = Path(audio_path)
    output_path = Path(output_path)

    start_time = time.perf_counter()
    config = get_transcription_config()
    model = create_whisper_model()

    logger.info(
        "Transcrevendo áudio: %s com beam_size=%s, vad_filter=%s",
        format_project_path(audio_path),
        config["beam_size"],
        config["vad_filter"],
    )

    segments, info = model.transcribe(
        str(audio_path),
        language=WHISPER_LANGUAGE,
        vad_filter=config["vad_filter"],
        vad_parameters=config["vad_parameters"],
        beam_size=config["beam_size"],
        best_of=config["best_of"],
        temperature=0,
        condition_on_previous_text=config["condition_on_previous_text"],
        word_timestamps=config["word_timestamps"],
    )

    transcript_segments = []
    for segment in segments:
        text = clean_transcript_text(segment.text)
        if not text:
            continue

        transcript_segments.append(
            TranscriptSegment(
                start=float(segment.start),
                end=float(segment.end),
                text=text,
            )
        )

    elapsed = time.perf_counter() - start_time
    audio_duration = float(getattr(info, "duration", 0) or 0)
    realtime_speed = audio_duration / elapsed if elapsed > 0 else 0
    metadata = TranscriptMetadata(
        execution_time_seconds=round(elapsed, 2),
        audio_duration_seconds=audio_duration,
        realtime_speed=round(realtime_speed, 2),
        segment_count=len(transcript_segments),
        model=WHISPER_MODEL,
        device=WHISPER_DEVICE,
        compute_type=WHISPER_COMPUTE_TYPE,
        beam_size=config["beam_size"],
        best_of=config["best_of"],
        vad_filter=config["vad_filter"],
        word_timestamps=config["word_timestamps"],
        profile=WHISPER_PROFILE,
        chunking_enabled=False,
    )

    transcript = Transcript(
        source_audio=format_project_path(audio_path),
        language=getattr(info, "language", WHISPER_LANGUAGE),
        duration=audio_duration,
        segments=transcript_segments,
        metadata=metadata,
    )

    save_json(
        transcript.model_dump(),
        output_path,
    )

    logger.info("Transcrição salva em: %s", format_project_path(output_path))
    logger.info("Tempo de transcrição: %.2fs", elapsed)
    logger.info("Duração do áudio: %.2fs", audio_duration)
    logger.info("Velocidade realtime: %.2fx", realtime_speed)
    logger.info("Segmentos gerados: %s", len(transcript_segments))
    logger.info("Perfil usado: %s", WHISPER_PROFILE)
    logger.info("word_timestamps: %s", config["word_timestamps"])

    return output_path


def transcribe_audio_by_chunks(
    audio_path: str | Path,
    output_path: str | Path,
    force: bool = False,
) -> Path:
    audio_path = Path(audio_path)
    output_path = Path(output_path)

    start_time = time.perf_counter()
    config = get_transcription_config()
    metadata = get_video_metadata(audio_path)
    audio_duration = float(metadata["duration"])
    chunk_ranges = build_chunk_ranges(
        audio_duration=audio_duration,
        chunk_duration=TRANSCRIPTION_CHUNK_DURATION,
        overlap=TRANSCRIPTION_CHUNK_OVERLAP,
    )

    if not chunk_ranges:
        raise ValueError(f"Não foi possível criar chunks para o áudio: {audio_path}")

    chunk_dir = (
        CACHE_TRANSCRIPTION_CHUNKS_DIR
        / audio_path.stem
        / f"duration_{TRANSCRIPTION_CHUNK_DURATION}_overlap_{TRANSCRIPTION_CHUNK_OVERLAP}"
    )
    chunk_dir.mkdir(parents=True, exist_ok=True)

    logger.info(
        "Transcrevendo áudio por chunks: %s chunks de até %ss",
        len(chunk_ranges),
        TRANSCRIPTION_CHUNK_DURATION,
    )

    chunk_jobs = []

    for chunk in chunk_ranges:
        chunk_audio_path = chunk_dir / f"chunk_{chunk['index']:03}.wav"
        chunk_json_path = chunk_dir / f"chunk_{chunk['index']:03}.json"

        if force or not chunk_audio_path.exists():
            create_audio_chunk(
                audio_path=audio_path,
                output_path=chunk_audio_path,
                start=chunk["start"],
                duration=chunk["duration"],
            )

        chunk_jobs.append(
            {
                "range": chunk,
                "audio_path": chunk_audio_path,
                "json_path": chunk_json_path,
            }
        )

    model = create_whisper_model()
    chunk_results = []

    if TRANSCRIPTION_CHUNKS_PARALLEL and TRANSCRIPTION_CHUNK_WORKERS > 1:
        workers = min(TRANSCRIPTION_CHUNK_WORKERS, len(chunk_jobs))
        logger.info("Transcrevendo chunks em paralelo com %s workers", workers)

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(
                    transcribe_chunk,
                    model,
                    job["audio_path"],
                    job["range"]["start"],
                    job["json_path"],
                    force,
                )
                for job in chunk_jobs
            ]

            for future in as_completed(futures):
                chunk_results.append(future.result())

        chunk_results = sorted(
            chunk_results,
            key=lambda item: item["chunk_start_offset"],
        )
    else:
        for job in chunk_jobs:
            result = transcribe_chunk(
                model=model,
                chunk_audio_path=job["audio_path"],
                chunk_start_offset=job["range"]["start"],
                output_path=job["json_path"],
                force=force,
            )
            chunk_results.append(result)

    merged_segments = merge_chunk_segments(chunk_results)
    transcript_segments = [
        TranscriptSegment(
            start=float(segment["start"]),
            end=float(segment["end"]),
            text=segment["text"],
        )
        for segment in merged_segments
    ]

    elapsed = time.perf_counter() - start_time
    realtime_speed = audio_duration / elapsed if elapsed > 0 else 0
    chunks_reused_from_cache = sum(
        1 for chunk in chunk_results if chunk.get("_reused_from_cache")
    )
    language = next(
        (
            chunk.get("language")
            for chunk in chunk_results
            if chunk.get("language")
        ),
        WHISPER_LANGUAGE,
    )
    chunk_metrics = [
        {
            "index": index,
            "chunk_audio": format_project_path(chunk.get("chunk_audio", "")),
            "chunk_start_offset": chunk.get("chunk_start_offset"),
            "duration": chunk.get("duration"),
            "execution_time_seconds": chunk.get("metadata", {}).get(
                "execution_time_seconds",
                0,
            ),
            "segment_count": chunk.get("metadata", {}).get("segment_count", 0),
            "reused_from_cache": bool(chunk.get("_reused_from_cache")),
        }
        for index, chunk in enumerate(chunk_results, start=1)
    ]

    transcript_metadata = TranscriptMetadata(
        execution_time_seconds=round(elapsed, 2),
        audio_duration_seconds=audio_duration,
        realtime_speed=round(realtime_speed, 2),
        segment_count=len(transcript_segments),
        model=WHISPER_MODEL,
        device=WHISPER_DEVICE,
        compute_type=WHISPER_COMPUTE_TYPE,
        beam_size=config["beam_size"],
        best_of=config["best_of"],
        vad_filter=config["vad_filter"],
        word_timestamps=config["word_timestamps"],
        profile=WHISPER_PROFILE,
        chunking_enabled=True,
        chunk_duration=TRANSCRIPTION_CHUNK_DURATION,
        chunk_overlap=TRANSCRIPTION_CHUNK_OVERLAP,
        chunk_count=len(chunk_ranges),
        chunks_reused_from_cache=chunks_reused_from_cache,
        chunk_metrics=chunk_metrics,
    )

    transcript = Transcript(
        source_audio=format_project_path(audio_path),
        language=language,
        duration=audio_duration,
        segments=transcript_segments,
        metadata=transcript_metadata,
    )

    save_json(transcript.model_dump(), output_path)

    logger.info("Transcrição salva em: %s", format_project_path(output_path))
    logger.info("Tempo de transcrição: %.2fs", elapsed)
    logger.info("Duração do áudio: %.2fs", audio_duration)
    logger.info("Velocidade realtime: %.2fx", realtime_speed)
    logger.info("Chunks gerados: %s", len(chunk_ranges))
    logger.info("Chunks reutilizados do cache: %s", chunks_reused_from_cache)
    logger.info("Segmentos gerados: %s", len(transcript_segments))
    logger.info("Perfil usado: %s", WHISPER_PROFILE)
    logger.info("word_timestamps: %s", config["word_timestamps"])

    return output_path
