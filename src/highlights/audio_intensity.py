import wave
from pathlib import Path
from typing import Iterable

import numpy as np


def read_wav_mono(audio_path: str | Path) -> tuple[np.ndarray, int]:
    with wave.open(str(audio_path), "rb") as wav:
        sample_rate = wav.getframerate()
        frames = wav.readframes(wav.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32)

    audio = audio / 32768.0

    return audio, sample_rate


def get_audio_energy(
    audio: np.ndarray,
    sample_rate: int,
    start: float,
    end: float,
) -> float:
    start_sample = int(start * sample_rate)
    end_sample = int(end * sample_rate)

    segment = audio[start_sample:end_sample]

    if len(segment) == 0:
        return 0.0

    rms = float(np.sqrt(np.mean(segment**2)))

    return rms


def normalize_energy(energy: float, max_energy: float) -> float:
    if max_energy <= 0:
        return 0.0

    return min(energy / max_energy, 1.0)


def get_wav_segment_energies(
    audio_path: str | Path,
    time_ranges: Iterable[tuple[float, float]],
) -> list[float]:
    energies = []

    with wave.open(str(audio_path), "rb") as wav:
        sample_rate = wav.getframerate()
        sample_width = wav.getsampwidth()

        if sample_width != 2:
            raise ValueError(f"Áudio WAV precisa estar em pcm_s16le: {audio_path}")

        for start, end in time_ranges:
            start_sample = max(int(start * sample_rate), 0)
            end_sample = max(int(end * sample_rate), start_sample)
            frame_count = end_sample - start_sample

            if frame_count == 0:
                energies.append(0.0)
                continue

            wav.setpos(min(start_sample, wav.getnframes()))
            frames = wav.readframes(frame_count)

            if not frames:
                energies.append(0.0)
                continue

            segment = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
            energies.append(float(np.sqrt(np.mean(segment**2))))

    return energies
