from collections import Counter, defaultdict
from pathlib import Path

from src.analytics.metrics_collector import VIDEO_METRICS_PATH, load_video_metrics
from src.analytics.video_metrics_schema import PerformancePattern, PerformanceReport
from src.config.paths import CACHE_ANALYTICS_DIR
from src.utils.file_utils import save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)

PERFORMANCE_REPORT_PATH = CACHE_ANALYTICS_DIR / "performance_report.json"
LEARNED_PATTERNS_PATH = CACHE_ANALYTICS_DIR / "learned_patterns.json"

TITLE_PATTERNS = [
    "NÃO ACREDITO",
    "AO VIVO",
    "INSANO",
    "ABSURDO",
    "INACREDITÁVEL",
]


def _average(values: list[float]) -> float:
    if not values:
        return 0.0

    return sum(values) / len(values)


def _top_performers(items: list, ratio: float = 0.3) -> list:
    if not items:
        return []

    sorted_items = sorted(
        items,
        key=lambda item: (
            item.retention_rate,
            item.click_through_rate,
            item.views,
        ),
        reverse=True,
    )
    limit = max(1, round(len(sorted_items) * ratio))

    return sorted_items[:limit]


def _has_real_metrics(item) -> bool:
    return any(
        [
            item.views > 0,
            item.likes > 0,
            item.comments > 0,
            item.shares > 0,
            item.retention_rate > 0,
            item.click_through_rate > 0,
            item.average_view_duration > 0,
        ]
    )


def _duration_range(items: list) -> list[int]:
    durations = [item.duration for item in items if item.duration > 0]

    if not durations:
        return []

    return [round(min(durations)), round(max(durations))]


def _best_emotions(items: list) -> list[str]:
    retention_by_emotion = defaultdict(list)

    for item in items:
        emotion = item.source_features.get("emotion")

        if emotion:
            retention_by_emotion[emotion].append(item.retention_rate)

    ranked = sorted(
        retention_by_emotion.items(),
        key=lambda entry: _average(entry[1]),
        reverse=True,
    )

    return [emotion for emotion, _retention in ranked[:3]]


def _preferred_title_patterns(items: list) -> list[str]:
    counter = Counter()

    for item in items:
        title = item.title.upper()

        for pattern in TITLE_PATTERNS:
            if pattern in title:
                counter[pattern] += 1

    return [pattern for pattern, _count in counter.most_common(3)]


def _sfx_penalty_threshold(items: list) -> int | None:
    by_sfx_count = defaultdict(list)

    for item in items:
        count = int(item.source_features.get("sfx_count", 0) or 0)
        by_sfx_count[count].append(item.retention_rate)

    if len(by_sfx_count) < 2:
        return None

    baseline = _average(by_sfx_count.get(0, []))

    for count, values in sorted(by_sfx_count.items()):
        if count > 0 and baseline and _average(values) < baseline:
            return count

    return None


def _preferred_zoom_intensity(items: list) -> float | None:
    intensities = [
        float(item.source_features.get("zoom_intensity", 0))
        for item in items
        if item.source_features.get("zoom_intensity")
    ]

    if not intensities:
        return None

    return round(_average(intensities), 2)


def analyze_video_performance(
    metrics_path: str | Path = VIDEO_METRICS_PATH,
    report_path: str | Path = PERFORMANCE_REPORT_PATH,
    learned_patterns_path: str | Path = LEARNED_PATTERNS_PATH,
) -> Path:
    dataset = load_video_metrics(metrics_path)
    items = [item for item in dataset.items if _has_real_metrics(item)]
    top_items = _top_performers(items)

    learned_patterns = {
        "best_short_duration_range": _duration_range(top_items),
        "best_emotions": _best_emotions(top_items),
        "preferred_title_patterns": _preferred_title_patterns(top_items),
        "sfx_penalty_if_more_than": _sfx_penalty_threshold(items),
        "zoom_preferred_intensity": _preferred_zoom_intensity(top_items),
    }

    patterns = [
        PerformancePattern(
            name=name,
            value=value,
            reason="calculado a partir dos vídeos com melhor retenção/CTR",
            sample_size=len(top_items),
        )
        for name, value in learned_patterns.items()
        if value not in (None, [], {})
    ]
    report = PerformanceReport(
        total_videos=len(items),
        average_retention_rate=round(
            _average([item.retention_rate for item in items]),
            4,
        ),
        average_click_through_rate=round(
            _average([item.click_through_rate for item in items]),
            4,
        ),
        patterns=patterns,
    )

    save_json(report.model_dump(), report_path)
    save_json(learned_patterns, learned_patterns_path)

    logger.info("Relatório de performance salvo em: %s", report_path)
    logger.info("Padrões aprendidos salvos em: %s", learned_patterns_path)

    return Path(report_path)
