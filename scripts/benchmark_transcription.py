import os
import subprocess
import sys
import time
import json
from pathlib import Path


CPU_THREADS_OPTIONS = [0, 2, 4]
NUM_WORKERS_OPTIONS = [1, 2, 4]


def parse_time_metrics(stderr: str) -> dict:
    metrics = {}

    for line in stderr.splitlines():
        line = line.strip()

        if line.startswith("User time (seconds):"):
            metrics["user_time_seconds"] = float(line.rsplit(":", 1)[1].strip())
        elif line.startswith("System time (seconds):"):
            metrics["system_time_seconds"] = float(line.rsplit(":", 1)[1].strip())
        elif line.startswith("Percent of CPU this job got:"):
            metrics["cpu_percent"] = line.rsplit(":", 1)[1].strip()
        elif line.startswith("Maximum resident set size (kbytes):"):
            metrics["max_rss_kb"] = int(line.rsplit(":", 1)[1].strip())

    return metrics


def load_transcript_metrics(output_path: Path) -> dict:
    if not output_path.exists():
        return {}

    with output_path.open("r", encoding="utf-8") as file:
        transcript = json.load(file)

    metadata = transcript.get("metadata", {})

    return {
        "execution_time_seconds": metadata.get("execution_time_seconds"),
        "realtime_speed": metadata.get("realtime_speed"),
        "segment_count": metadata.get("segment_count"),
        "chunk_count": metadata.get("chunk_count"),
        "chunks_reused_from_cache": metadata.get("chunks_reused_from_cache"),
        "sample_segments": transcript.get("segments", [])[:3],
    }


def main() -> None:
    audio_path = Path(
        os.getenv(
            "BENCHMARK_AUDIO_PATH",
            "cache/audio/audio.wav",
        )
    )

    if not audio_path.exists():
        raise FileNotFoundError(
            "Defina BENCHMARK_AUDIO_PATH apontando para um WAV curto."
        )

    output_dir = Path(os.getenv("BENCHMARK_OUTPUT_DIR", "cache/transcripts/benchmarks"))
    output_dir.mkdir(parents=True, exist_ok=True)
    benchmark_report_path = output_dir / "benchmark_results.json"
    results = []

    for cpu_threads in CPU_THREADS_OPTIONS:
        for num_workers in NUM_WORKERS_OPTIONS:
            output_path = (
                output_dir / f"transcript_cpu{cpu_threads}_workers{num_workers}.json"
            )

            env = os.environ.copy()
            env["WHISPER_CPU_THREADS"] = str(cpu_threads)
            env["WHISPER_NUM_WORKERS"] = str(num_workers)
            env["TRANSCRIPTION_USE_CHUNKS"] = "true"
            env["TRANSCRIPTION_CHUNKS_PARALLEL"] = env.get(
                "TRANSCRIPTION_CHUNKS_PARALLEL",
                "false",
            )
            env["TRANSCRIPTION_CHUNK_DURATION"] = env.get(
                "BENCHMARK_CHUNK_DURATION",
                "300",
            )

            started_at = time.perf_counter()
            process = subprocess.run(
                [
                    "/usr/bin/time",
                    "-v",
                    sys.executable,
                    "-c",
                    (
                        "from src.transcription.whisper_transcriber "
                        "import transcribe_audio; "
                        f"transcribe_audio({str(audio_path)!r}, "
                        f"output_path={str(output_path)!r}, force=True)"
                    ),
                ],
                capture_output=True,
                text=True,
                env=env,
            )
            elapsed = time.perf_counter() - started_at
            time_metrics = parse_time_metrics(process.stderr)
            transcript_metrics = load_transcript_metrics(output_path)

            result = {
                "cpu_threads": cpu_threads,
                "num_workers": num_workers,
                "status": "ok" if process.returncode == 0 else "error",
                "wall_time_seconds": round(elapsed, 2),
                "output_path": str(output_path),
                "stdout_tail": process.stdout.splitlines()[-20:],
                "stderr_tail": process.stderr.splitlines()[-20:],
                **time_metrics,
                **transcript_metrics,
            }

            results.append(result)

            with benchmark_report_path.open("w", encoding="utf-8") as file:
                json.dump(
                    {
                        "audio_path": str(audio_path),
                        "chunk_duration": int(env["TRANSCRIPTION_CHUNK_DURATION"]),
                        "chunks_parallel": env["TRANSCRIPTION_CHUNKS_PARALLEL"],
                        "results": results,
                    },
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            if process.returncode != 0:
                print(f"Falha no benchmark: {result}")
                process.check_returncode()

    print("Benchmark de transcrição:")
    for result in results:
        print(
            "cpu_threads={cpu_threads} num_workers={num_workers} "
            "tempo={execution_time_seconds}s realtime={realtime_speed}x "
            "segmentos={segment_count} rss={max_rss_kb}KB output={output_path}".format(
                **result
            )
        )
    print(f"Relatório salvo em: {benchmark_report_path}")


if __name__ == "__main__":
    main()
