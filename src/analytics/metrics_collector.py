import csv
from pathlib import Path

from src.analytics.video_metrics_schema import VideoMetrics, VideoMetricsDataset
from src.config.paths import CACHE_ANALYTICS_DIR, DATA_ANALYTICS_DIR
from src.utils.file_utils import load_json, save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)

MANUAL_METRICS_CSV = DATA_ANALYTICS_DIR / "manual_video_metrics.csv"
VIDEO_METRICS_PATH = CACHE_ANALYTICS_DIR / "video_metrics.json"


def _to_int(value: str | None) -> int:
    if not value:
        return 0

    return int(float(value))


def _to_float(value: str | None) -> float:
    if not value:
        return 0.0

    return float(value)


def _index_shorts_by_id(edit_plan: dict) -> dict[str, dict]:
    return {
        short["id"]: short
        for short in edit_plan.get("shorts", [])
    }


def _source_features_from_short(short: dict | None) -> dict:
    if not short:
        return {}

    actions = short.get("actions", [])
    zoom_actions = [action for action in actions if action.get("type") == "zoom"]
    sfx_actions = [action for action in actions if action.get("type") == "sfx"]

    return {
        "highlight_score": short.get("score", 0),
        "emotion": short.get("emotion"),
        "style": short.get("style"),
        "had_zoom": bool(zoom_actions),
        "zoom_intensity": max(
            (action.get("intensity", 0) or 0 for action in zoom_actions),
            default=0,
        ),
        "had_sfx": bool(sfx_actions),
        "sfx_count": len(sfx_actions),
        "subtitle_style": "bold_clean",
    }


def load_video_metrics(path: str | Path = VIDEO_METRICS_PATH) -> VideoMetricsDataset:
    path = Path(path)

    if not path.exists():
        return VideoMetricsDataset()

    return VideoMetricsDataset.model_validate(load_json(path))


def collect_manual_video_metrics(
    csv_path: str | Path = MANUAL_METRICS_CSV,
    edit_plan_path: str | Path | None = None,
    output_path: str | Path = VIDEO_METRICS_PATH,
) -> Path:
    csv_path = Path(csv_path)
    output_path = Path(output_path)

    if not csv_path.exists():
        logger.warning("CSV manual de métricas não encontrado: %s", csv_path)
        save_json(VideoMetricsDataset().model_dump(), output_path)
        return output_path

    shorts_by_id = {}

    if edit_plan_path is not None and Path(edit_plan_path).exists():
        edit_plan = load_json(edit_plan_path)
        shorts_by_id = _index_shorts_by_id(edit_plan)

    items = []

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            video_id = row["video_id"]
            short = shorts_by_id.get(video_id)
            duration = _to_float(row.get("duration")) or (
                float(short.get("duration", 0)) if short else 0
            )
            title = row.get("title") or (short.get("title", "") if short else "")

            items.append(
                VideoMetrics(
                    video_id=video_id,
                    platform=row.get("platform", ""),
                    title=title,
                    duration=duration,
                    views=_to_int(row.get("views")),
                    likes=_to_int(row.get("likes")),
                    comments=_to_int(row.get("comments")),
                    shares=_to_int(row.get("shares")),
                    watch_time_seconds=_to_float(row.get("watch_time_seconds")),
                    average_view_duration=_to_float(row.get("average_view_duration")),
                    retention_rate=_to_float(
                        row.get("retention_rate") or row.get("retention")
                    ),
                    click_through_rate=_to_float(row.get("ctr")),
                    published_at=row.get("published_at") or None,
                    source_features=_source_features_from_short(short),
                )
            )

    dataset = VideoMetricsDataset(items=items)
    save_json(dataset.model_dump(), output_path)
    logger.info("Métricas de vídeos coletadas: %s", len(items))
    logger.info("Métricas salvas em: %s", output_path)

    return output_path
