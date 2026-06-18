from pathlib import Path

from src.publishing import publish_planner
from src.publishing.instagram_publisher import publish_to_instagram
from src.publishing.scheduler import schedule_publish_item
from src.publishing.tiktok_publisher import publish_to_tiktok
from src.publishing.youtube_publisher import publish_to_youtube
from src.utils.file_utils import load_json


def test_generate_publish_plan_creates_safe_pending_items(
    tmp_path: Path,
    monkeypatch,
) -> None:
    shorts_dir = tmp_path / "output" / "shorts"
    long_dir = tmp_path / "output" / "long"
    cache_dir = tmp_path / "cache" / "publishing"
    shorts_dir.mkdir(parents=True)
    long_dir.mkdir(parents=True)

    (shorts_dir / "short_02.mp4").write_bytes(b"short 2")
    (shorts_dir / "short_01.mp4").write_bytes(b"short 1")
    (long_dir / "video_01.mp4").write_bytes(b"long")

    monkeypatch.setattr(publish_planner, "OUTPUT_SHORTS_DIR", shorts_dir)
    monkeypatch.setattr(publish_planner, "OUTPUT_LONG_DIR", long_dir)
    monkeypatch.setattr(publish_planner, "CACHE_PUBLISH_DIR", cache_dir)

    publish_plan_path = publish_planner.generate_publish_plan()

    assert publish_plan_path == cache_dir / "publish_plan.json"
    assert load_json(publish_plan_path) == {
        "items": [
            {
                "platform": "youtube_shorts",
                "video_path": str(shorts_dir / "short_01.mp4"),
                "title": "SHORT 01",
                "description": (
                    "Short gerado automaticamente pelo Video AI Editor."
                ),
                "tags": ["shorts", "live", "gameplay"],
                "scheduled_at": None,
                "privacy_status": "private",
                "status": "pending",
            },
            {
                "platform": "youtube_shorts",
                "video_path": str(shorts_dir / "short_02.mp4"),
                "title": "SHORT 02",
                "description": (
                    "Short gerado automaticamente pelo Video AI Editor."
                ),
                "tags": ["shorts", "live", "gameplay"],
                "scheduled_at": None,
                "privacy_status": "private",
                "status": "pending",
            },
            {
                "platform": "youtube",
                "video_path": str(long_dir / "video_01.mp4"),
                "title": "Melhores momentos da live",
                "description": "Vídeo gerado automaticamente pelo Video AI Editor.",
                "tags": ["gameplay", "live", "melhores momentos"],
                "scheduled_at": None,
                "privacy_status": "private",
                "status": "pending",
            },
        ]
    }


def test_publishers_are_safe_placeholders() -> None:
    item = {
        "platform": "youtube_shorts",
        "video_path": "output/shorts/short_01.mp4",
    }

    assert publish_to_youtube(item)["status"] == "not_implemented"
    assert publish_to_tiktok(item)["status"] == "not_implemented"
    assert publish_to_instagram(item)["status"] == "not_implemented"
    assert schedule_publish_item(item)["status"] == "not_implemented"
