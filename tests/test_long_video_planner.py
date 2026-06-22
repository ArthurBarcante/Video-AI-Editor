from src.planning.long_video_planner import plan_long_videos


def test_plan_long_videos_skips_too_short_compilation() -> None:
    highlights = [
        {
            "start": 10.0,
            "end": 15.0,
            "text": "momento curto",
            "score": 0.8,
            "reasons": ["teste"],
        }
    ]

    assert plan_long_videos(highlights) == []


def test_plan_long_videos_keeps_publishable_short_compilation() -> None:
    highlights = [
        {
            "start": 100.0,
            "end": 155.0,
            "text": "momento longo",
            "score": 0.8,
            "reasons": ["teste"],
        }
    ]

    long_videos = plan_long_videos(highlights)

    assert len(long_videos) == 1
    assert long_videos[0].theme == "compilado curto de melhores momentos"
