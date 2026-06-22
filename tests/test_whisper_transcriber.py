from pathlib import Path
from types import SimpleNamespace

import pytest

from src.config.paths import ROOT_DIR
from src.transcription import whisper_transcriber
from src.transcription.whisper_transcriber import (
    transcribe_audio,
    transcribe_audio_by_chunks,
)
from src.utils.file_utils import load_json, save_json


class FakeWhisperModel:
    created_instances = []

    def __init__(
        self,
        model_name: str,
        *,
        device: str,
        compute_type: str,
        cpu_threads: int,
        num_workers: int,
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self.cpu_threads = cpu_threads
        self.num_workers = num_workers
        self.transcribe_calls = []
        FakeWhisperModel.created_instances.append(self)

    def transcribe(self, audio_path: str, **kwargs: object) -> tuple[list[object], object]:
        self.transcribe_calls.append((audio_path, kwargs))
        return (
            [
                SimpleNamespace(start=0.0, end=1.0, text=" Olá mundo "),
                SimpleNamespace(start=1.0, end=1.5, text="   "),
                SimpleNamespace(start=1.5, end=3.2, text="próxima fala"),
            ],
            SimpleNamespace(language="pt", duration=3.2),
        )


@pytest.fixture(autouse=True)
def reset_fake_model() -> None:
    FakeWhisperModel.created_instances = []


def test_transcribe_audio_generates_valid_json(
    monkeypatch: pytest.MonkeyPatch,
    sample_audio: Path,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "cache" / "transcripts" / "sample_transcript.json"
    monkeypatch.setattr(
        whisper_transcriber,
        "get_whisper_model_class",
        lambda: FakeWhisperModel,
    )
    monkeypatch.setattr(whisper_transcriber, "TRANSCRIPTION_USE_CHUNKS", False)

    transcript_path = transcribe_audio(sample_audio, output_path=output_path)
    transcript = load_json(transcript_path)

    assert transcript_path == output_path
    assert transcript["source_audio"].endswith("sample.wav")
    assert transcript["language"] == "pt"
    assert transcript["duration"] == 3.2
    assert transcript["segments"] == [
        {"start": 0.0, "end": 1.0, "text": "Olá mundo"},
        {"start": 1.5, "end": 3.2, "text": "próxima fala"},
    ]
    assert transcript["metadata"]["audio_duration_seconds"] == 3.2
    assert transcript["metadata"]["segment_count"] == 2
    assert transcript["metadata"]["model"] == whisper_transcriber.WHISPER_MODEL
    assert transcript["metadata"]["device"] == whisper_transcriber.WHISPER_DEVICE
    assert transcript["metadata"]["compute_type"] == whisper_transcriber.WHISPER_COMPUTE_TYPE
    assert transcript["metadata"]["beam_size"] == 1
    assert transcript["metadata"]["best_of"] == 1
    assert transcript["metadata"]["vad_filter"] is True
    assert transcript["metadata"]["word_timestamps"] is False
    assert transcript["metadata"]["profile"] == "fast"
    assert transcript["metadata"]["execution_time_seconds"] >= 0
    assert transcript["metadata"]["realtime_speed"] >= 0

    instance = FakeWhisperModel.created_instances[0]
    assert instance.model_name == whisper_transcriber.WHISPER_MODEL
    assert instance.device == whisper_transcriber.WHISPER_DEVICE
    assert instance.compute_type == whisper_transcriber.WHISPER_COMPUTE_TYPE
    assert instance.cpu_threads == whisper_transcriber.WHISPER_CPU_THREADS
    assert instance.num_workers == whisper_transcriber.WHISPER_NUM_WORKERS
    assert instance.transcribe_calls[0][1]["language"] == "pt"
    assert instance.transcribe_calls[0][1]["vad_filter"] is True
    assert instance.transcribe_calls[0][1]["vad_parameters"] == {
        "min_silence_duration_ms": 500,
    }
    assert instance.transcribe_calls[0][1]["beam_size"] == 1
    assert instance.transcribe_calls[0][1]["best_of"] == 1
    assert instance.transcribe_calls[0][1]["temperature"] == 0
    assert (
        instance.transcribe_calls[0][1]["condition_on_previous_text"]
        is whisper_transcriber.WHISPER_CONDITION_ON_PREVIOUS_TEXT
    )
    assert instance.transcribe_calls[0][1]["word_timestamps"] is False


def test_transcribe_audio_uses_cache_without_force(
    monkeypatch: pytest.MonkeyPatch,
    sample_audio: Path,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "cache" / "transcripts" / "sample_transcript.json"
    save_json({"cached": True}, output_path)
    monkeypatch.setattr(
        whisper_transcriber,
        "get_whisper_model_class",
        lambda: FakeWhisperModel,
    )
    monkeypatch.setattr(whisper_transcriber, "TRANSCRIPTION_USE_CHUNKS", False)

    transcript_path = transcribe_audio(sample_audio, output_path=output_path)

    assert transcript_path == output_path
    assert load_json(transcript_path) == {"cached": True}
    assert FakeWhisperModel.created_instances == []


def test_transcribe_audio_force_retranscribes_existing_file(
    monkeypatch: pytest.MonkeyPatch,
    sample_audio: Path,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "cache" / "transcripts" / "sample_transcript.json"
    save_json({"cached": True}, output_path)
    monkeypatch.setattr(
        whisper_transcriber,
        "get_whisper_model_class",
        lambda: FakeWhisperModel,
    )
    monkeypatch.setattr(whisper_transcriber, "TRANSCRIPTION_USE_CHUNKS", False)

    transcribe_audio(sample_audio, output_path=output_path, force=True)

    assert load_json(output_path)["segments"][0]["text"] == "Olá mundo"
    assert len(FakeWhisperModel.created_instances) == 1


def test_transcribe_audio_rejects_project_root_output(sample_audio: Path) -> None:
    with pytest.raises(ValueError, match="cache/ ou output"):
        transcribe_audio(sample_audio, output_path=ROOT_DIR / "transcript.json")


def test_transcribe_audio_rejects_missing_audio(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Áudio não encontrado"):
        transcribe_audio(tmp_path / "missing.wav")


def test_transcribe_audio_rejects_non_wav(tmp_path: Path) -> None:
    audio_path = tmp_path / "sample.mp3"
    audio_path.write_bytes(b"not wav")

    with pytest.raises(ValueError, match="não é .wav"):
        transcribe_audio(audio_path)


def test_transcribe_audio_by_chunks_generates_partial_cache(
    monkeypatch: pytest.MonkeyPatch,
    sample_audio: Path,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "cache" / "transcripts" / "sample_transcript.json"
    chunk_dir = tmp_path / "cache" / "transcripts" / "chunks"
    created_chunks = []

    def fake_create_audio_chunk(
        audio_path: str | Path,
        output_path: str | Path,
        start: float,
        duration: float,
    ) -> Path:
        created_chunks.append((audio_path, output_path, start, duration))
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(b"chunk")
        return Path(output_path)

    monkeypatch.setattr(
        whisper_transcriber,
        "get_whisper_model_class",
        lambda: FakeWhisperModel,
    )
    monkeypatch.setattr(
        whisper_transcriber,
        "get_video_metadata",
        lambda audio_path: {"duration": 20.0},
    )
    monkeypatch.setattr(
        whisper_transcriber,
        "create_audio_chunk",
        fake_create_audio_chunk,
    )
    monkeypatch.setattr(
        whisper_transcriber,
        "CACHE_TRANSCRIPTION_CHUNKS_DIR",
        chunk_dir,
    )
    monkeypatch.setattr(whisper_transcriber, "TRANSCRIPTION_CHUNK_DURATION", 10)
    monkeypatch.setattr(whisper_transcriber, "TRANSCRIPTION_CHUNK_OVERLAP", 2)
    monkeypatch.setattr(whisper_transcriber, "TRANSCRIPTION_CHUNKS_PARALLEL", False)

    transcript_path = transcribe_audio_by_chunks(
        sample_audio,
        output_path=output_path,
    )
    transcript = load_json(transcript_path)

    assert transcript["duration"] == 20.0
    assert transcript["metadata"]["chunking_enabled"] is True
    assert transcript["metadata"]["chunk_duration"] == 10
    assert transcript["metadata"]["chunk_overlap"] == 2
    assert transcript["metadata"]["chunk_count"] == 3
    assert transcript["metadata"]["chunks_reused_from_cache"] == 0
    assert transcript["metadata"]["segment_count"] == 6
    assert transcript["segments"][2]["start"] == 8.0
    cache_dir = chunk_dir / sample_audio.stem / "duration_10_overlap_2"
    assert (cache_dir / "chunk_001.json").exists()
    assert (cache_dir / "chunk_002.json").exists()
    assert (cache_dir / "chunk_003.json").exists()
    assert len(created_chunks) == 3

    transcript_path = transcribe_audio_by_chunks(
        sample_audio,
        output_path=output_path,
    )
    cached_transcript = load_json(transcript_path)

    assert cached_transcript["metadata"]["chunks_reused_from_cache"] == 3
    assert len(FakeWhisperModel.created_instances) == 2
