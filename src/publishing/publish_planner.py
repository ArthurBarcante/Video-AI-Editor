from pathlib import Path

from src.config.paths import CACHE_PUBLISH_DIR, OUTPUT_LONG_DIR, OUTPUT_SHORTS_DIR
from src.publishing.publish_schema import PublishPlan, PublishTarget
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.utils.cache_metadata import is_cache_valid, save_cache_metadata
from src.utils.file_utils import format_project_path, save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def _build_short_target(video: Path) -> PublishTarget:
    return PublishTarget(
        platform="youtube_shorts",
        video_path=format_project_path(video),
        title=video.stem.replace("_", " ").upper(),
        description="Short gerado automaticamente pelo Video AI Editor.",
        tags=["shorts", "live", "gameplay"],
        privacy_status="private",
    )


def _build_long_target(video: Path) -> PublishTarget:
    return PublishTarget(
        platform="youtube",
        video_path=format_project_path(video),
        title="Melhores momentos da live",
        description="Vídeo gerado automaticamente pelo Video AI Editor.",
        tags=["gameplay", "live", "melhores momentos"],
        privacy_status="private",
    )


def generate_publish_plan(
    force: bool = False,
    short_paths: list[str | Path] | None = None,
    long_video_paths: list[str | Path] | None = None,
) -> Path:
    output_path = CACHE_PUBLISH_DIR / "publish_plan.json"
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if short_paths is None:
        short_paths = sorted(OUTPUT_SHORTS_DIR.glob("*.mp4"))
    else:
        short_paths = sorted(Path(path) for path in short_paths)

    if long_video_paths is None:
        long_video_paths = sorted(OUTPUT_LONG_DIR.glob("*.mp4"))
    else:
        long_video_paths = sorted(Path(path) for path in long_video_paths)

    cache_sources = [*short_paths, *long_video_paths]

    if output_path.exists() and not force and is_cache_valid(output_path, cache_sources):
        logger.info("Publish plan já existe: %s", format_project_path(output_path))
        return output_path

    items = []

    for video in short_paths:
        items.append(_build_short_target(video))

    for video in long_video_paths:
        items.append(_build_long_target(video))

    plan = PublishPlan(items=items)
    save_json(plan.model_dump(), output_path)
    save_cache_metadata(output_path, cache_sources)

    logger.info("Publish plan gerado: %s", format_project_path(output_path))

    return output_path
