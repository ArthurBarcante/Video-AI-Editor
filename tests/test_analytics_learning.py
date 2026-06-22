from src.analytics.learning_from_metrics import apply_metrics_to_learning_profile
from src.analytics.metrics_collector import collect_manual_video_metrics, load_video_metrics
from src.analytics.performance_analyzer import analyze_video_performance
from src.learning.correction_memory import load_learning_profile, save_learning_profile
from src.learning.feedback_schema import LearningProfile
from src.utils.file_utils import load_json, save_json


def test_collect_manual_video_metrics_enriches_with_edit_plan(tmp_path) -> None:
    csv_path = tmp_path / "manual_video_metrics.csv"
    edit_plan_path = tmp_path / "edit_plan.json"
    output_path = tmp_path / "video_metrics.json"

    csv_path.write_text(
        "\n".join(
            [
                "video_id,platform,views,likes,comments,shares,average_view_duration,retention_rate,ctr",
                "short_01,youtube_shorts,12000,930,45,80,23.8,0.73,0.09",
            ]
        ),
        encoding="utf-8",
    )
    save_json(
        {
            "source_video": "input/live.mp4",
            "shorts": [
                {
                    "id": "short_01",
                    "start": 10.0,
                    "end": 42.0,
                    "duration": 32.0,
                    "score": 0.87,
                    "title": "EU NÃO ACREDITO QUE ISSO ACONTECEU",
                    "reason": "surpresa",
                    "style": "intense",
                    "actions": [
                        {
                            "type": "zoom",
                            "intensity": 1.12,
                        },
                        {
                            "type": "sfx",
                            "name": "pop",
                        },
                    ],
                }
            ],
            "long_videos": [],
        },
        edit_plan_path,
    )

    collect_manual_video_metrics(csv_path, edit_plan_path, output_path)
    dataset = load_video_metrics(output_path)

    assert dataset.items[0].video_id == "short_01"
    assert dataset.items[0].duration == 32.0
    assert dataset.items[0].title == "EU NÃO ACREDITO QUE ISSO ACONTECEU"
    assert dataset.items[0].source_features["had_zoom"] is True
    assert dataset.items[0].source_features["sfx_count"] == 1


def test_analyze_video_performance_generates_patterns(tmp_path) -> None:
    metrics_path = tmp_path / "video_metrics.json"
    report_path = tmp_path / "performance_report.json"
    learned_patterns_path = tmp_path / "learned_patterns.json"

    save_json(
        {
            "items": [
                {
                    "video_id": "short_01",
                    "platform": "youtube_shorts",
                    "title": "EU NÃO ACREDITO QUE ISSO ACONTECEU",
                    "duration": 32.0,
                    "views": 12000,
                    "likes": 930,
                    "comments": 45,
                    "shares": 80,
                    "watch_time_seconds": 280000,
                    "average_view_duration": 23.8,
                    "retention_rate": 0.73,
                    "click_through_rate": 0.09,
                    "published_at": "2026-06-22T18:00:00",
                    "source_features": {
                        "emotion": "surprise",
                        "zoom_intensity": 1.12,
                        "sfx_count": 1,
                    },
                },
                {
                    "video_id": "short_02",
                    "platform": "youtube_shorts",
                    "title": "MOMENTO DA LIVE",
                    "duration": 45.0,
                    "views": 1000,
                    "likes": 40,
                    "comments": 2,
                    "shares": 1,
                    "watch_time_seconds": 10000,
                    "average_view_duration": 12.0,
                    "retention_rate": 0.26,
                    "click_through_rate": 0.02,
                    "source_features": {
                        "emotion": "neutral",
                        "zoom_intensity": 1.35,
                        "sfx_count": 3,
                    },
                },
            ]
        },
        metrics_path,
    )

    analyze_video_performance(metrics_path, report_path, learned_patterns_path)
    report = load_json(report_path)
    learned = load_json(learned_patterns_path)

    assert report["total_videos"] == 2
    assert learned["best_short_duration_range"] == [32, 32]
    assert learned["best_emotions"] == ["surprise"]
    assert learned["preferred_title_patterns"] == ["NÃO ACREDITO"]
    assert learned["zoom_preferred_intensity"] == 1.12


def test_analyze_video_performance_ignores_empty_manual_rows(tmp_path) -> None:
    metrics_path = tmp_path / "video_metrics.json"
    report_path = tmp_path / "performance_report.json"
    learned_patterns_path = tmp_path / "learned_patterns.json"

    save_json(
        {
            "items": [
                {
                    "video_id": "short_01",
                    "platform": "youtube_shorts",
                    "title": "SHORT 01",
                    "duration": 15.0,
                    "views": 0,
                    "likes": 0,
                    "comments": 0,
                    "shares": 0,
                    "watch_time_seconds": 0,
                    "average_view_duration": 0,
                    "retention_rate": 0,
                    "click_through_rate": 0,
                    "source_features": {
                        "zoom_intensity": 1.15,
                    },
                }
            ]
        },
        metrics_path,
    )

    analyze_video_performance(metrics_path, report_path, learned_patterns_path)
    report = load_json(report_path)
    learned = load_json(learned_patterns_path)

    assert report["total_videos"] == 0
    assert report["patterns"] == []
    assert learned["best_short_duration_range"] == []
    assert learned["zoom_preferred_intensity"] is None


def test_apply_metrics_to_learning_profile_updates_analytics_learning(tmp_path) -> None:
    learned_patterns_path = tmp_path / "learned_patterns.json"
    profile_path = tmp_path / "learning_profile.json"

    save_json(
        {
            "best_short_duration_range": [25, 35],
            "best_emotions": ["surprise", "hype"],
            "preferred_title_patterns": ["NÃO ACREDITO"],
            "sfx_penalty_if_more_than": 2,
            "zoom_preferred_intensity": 1.12,
        },
        learned_patterns_path,
    )
    save_learning_profile(LearningProfile(), profile_path)

    apply_metrics_to_learning_profile(learned_patterns_path, profile_path)
    profile = load_learning_profile(profile_path)

    assert profile.analytics_learning["best_short_duration_range"] == [25, 35]
    assert profile.analytics_learning["best_emotions"] == ["surprise", "hype"]
