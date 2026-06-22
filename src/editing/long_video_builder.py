import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from src.config.paths import OUTPUT_LONG_DIR
from src.config.settings import (
    LONG_AUDIO_COPY,
    LONG_RENDER_PARALLEL,
    LONG_RENDER_PROFILE,
    LONG_RENDER_WORKERS,
)
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path, run_command
from src.rendering.render_profiles import get_render_profile
from src.utils.cache_metadata import is_cache_valid, save_cache_metadata
from src.utils.file_utils import format_project_path, load_json, save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def cut_segment(
    source_video: str | Path,
    segment: dict,
    output_path: str | Path,
) -> dict:
    source_video = Path(source_video)
    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    started_at = time.perf_counter()
    profile = get_render_profile(LONG_RENDER_PROFILE)

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(segment["start"]),
        "-i",
        str(source_video),
        "-t",
        str(segment["duration"]),
        "-c:v",
        profile["video_codec"],
        "-preset",
        profile["preset"],
        "-crf",
        profile["crf"],
    ]

    if LONG_AUDIO_COPY:
        command.extend(["-c:a", "copy"])
    else:
        command.extend(["-c:a", profile["audio_codec"]])

    command.extend(
        [
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )

    run_command(command)

    elapsed = time.perf_counter() - started_at
    start = segment["start"]
    end = segment.get("end", start + segment["duration"])

    logger.info(
        "Segmento %s cortado em %.2fs usando perfil %s",
        segment.get("id", output_path.stem),
        elapsed,
        LONG_RENDER_PROFILE,
    )

    return {
        "path": output_path,
        "segment_id": segment.get("id"),
        "start": start,
        "end": end,
        "duration": segment["duration"],
        "execution_time_seconds": round(elapsed, 2),
    }


def concat_segments(segment_paths: list[Path], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    concat_file = output_path.parent / f"{output_path.stem}_concat.txt"

    lines = [
        f"file '{segment_path.resolve()}'"
        for segment_path in segment_paths
    ]

    concat_file.write_text("\n".join(lines), encoding="utf-8")

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(output_path),
    ]

    run_command(command)

    concat_file.unlink(missing_ok=True)

    return output_path


def render_long_video(
    source_video: str | Path,
    long_video: dict,
    output_dir: str | Path | None = None,
    force: bool = False,
    cache_sources: list[str | Path] | None = None,
) -> Path:
    source_video = Path(source_video)
    if output_dir is None:
        output_dir = OUTPUT_LONG_DIR

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{long_video['id']}.mp4"
    ensure_safe_project_output_path(output_path)

    if cache_sources is None:
        cache_sources = [source_video]

    if output_path.exists() and not force and is_cache_valid(output_path, cache_sources):
        logger.info("Vídeo longo já existe: %s", format_project_path(output_path))
        return output_path

    segments = long_video.get("segments", [])

    if not segments:
        raise ValueError(f"Nenhum segmento encontrado para {long_video['id']}")

    started_at = time.perf_counter()
    logger.info("Renderizando vídeo longo: %s", long_video["id"])

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        segment_results = []

        if LONG_RENDER_PARALLEL and LONG_RENDER_WORKERS > 1:
            workers = min(LONG_RENDER_WORKERS, len(segments))

            logger.info(
                "Cortando segmentos em paralelo com %s workers",
                workers,
            )

            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = []

                for index, segment in enumerate(segments, start=1):
                    segment = segment.copy()
                    segment["id"] = f"segment_{index:03}"

                    segment_path = temp_dir / f"segment_{index:03}.mp4"

                    futures.append(
                        executor.submit(
                            cut_segment,
                            source_video,
                            segment,
                            segment_path,
                        )
                    )

                for future in as_completed(futures):
                    segment_results.append(future.result())

            segment_results = sorted(segment_results, key=lambda item: item["path"])
        else:
            for index, segment in enumerate(segments, start=1):
                segment = segment.copy()
                segment["id"] = f"segment_{index:03}"

                segment_path = temp_dir / f"segment_{index:03}.mp4"

                result = cut_segment(
                    source_video=source_video,
                    segment=segment,
                    output_path=segment_path,
                )

                segment_results.append(result)

        segment_paths = [item["path"] for item in segment_results]
        concat_segments(segment_paths, output_path)

    elapsed = time.perf_counter() - started_at
    report_path = output_path.with_suffix(".json")
    report = {
        "id": long_video["id"],
        "output_path": str(output_path),
        "segment_count": len(segment_results),
        "planned_duration": sum(item["duration"] for item in segment_results),
        "total_execution_time_seconds": round(elapsed, 2),
        "render_profile": LONG_RENDER_PROFILE,
        "parallel": LONG_RENDER_PARALLEL,
        "workers": LONG_RENDER_WORKERS,
        "audio_copy": LONG_AUDIO_COPY,
        "segments": [
            {
                "id": item["segment_id"],
                "start": item["start"],
                "end": item["end"],
                "duration": item["duration"],
                "execution_time_seconds": item["execution_time_seconds"],
            }
            for item in segment_results
        ],
    }
    save_json(report, report_path)
    save_cache_metadata(output_path, cache_sources)

    logger.info("Vídeo longo exportado: %s", format_project_path(output_path))
    logger.info("Tempo total vídeo longo: %.2fs", elapsed)
    logger.info("Relatório do vídeo longo salvo em: %s", format_project_path(report_path))

    return output_path


def render_long_videos_from_edit_plan(
    edit_plan_path: str | Path,
    force: bool = False,
) -> list[Path]:
    edit_plan = load_json(edit_plan_path)
    edit_plan_path = Path(edit_plan_path)

    source_video = edit_plan["source_video"]
    cache_sources = [edit_plan_path, source_video]
    long_videos = edit_plan.get("long_videos", [])

    rendered = []

    for long_video in long_videos:
        output_path = render_long_video(
            source_video=source_video,
            long_video=long_video,
            force=force,
            cache_sources=cache_sources,
        )

        rendered.append(output_path)

    logger.info("Vídeos longos renderizados: %s", len(rendered))

    return rendered
