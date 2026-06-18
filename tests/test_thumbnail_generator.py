from pathlib import Path

from PIL import Image

from src.thumbnails import frame_capture, thumbnail_generator
from src.thumbnails.frame_capture import capture_frame
from src.thumbnails.thumbnail_generator import (
    add_text_to_thumbnail,
    generate_thumbnails_from_edit_plan,
)
from src.thumbnails.thumbnail_selector import (
    select_best_shorts_for_thumbnails,
    select_thumbnail_timestamp,
)
from src.utils.file_utils import save_json


def test_select_thumbnail_timestamp_uses_middle_of_item() -> None:
    assert select_thumbnail_timestamp({"start": 10.0, "end": 20.0}) == 15.0


def test_select_best_shorts_for_thumbnails_orders_by_score() -> None:
    shorts = [
        {"id": "short_02", "score": 0.5},
        {"id": "short_01", "score": 0.9},
    ]

    assert select_best_shorts_for_thumbnails(shorts) == [
        {"id": "short_01", "score": 0.9},
        {"id": "short_02", "score": 0.5},
    ]


def test_capture_frame_builds_expected_ffmpeg_command(
    monkeypatch,
    tmp_path: Path,
) -> None:
    calls = []
    output_path = tmp_path / "output" / "thumbnails" / "frame.jpg"

    def fake_run_command(command: list[str]) -> None:
        calls.append(command)
        output_path.write_bytes(b"frame")

    monkeypatch.setattr(frame_capture, "run_command", fake_run_command)

    result = capture_frame(
        video_path="input/live.mp4",
        timestamp=12.5,
        output_path=output_path,
    )

    assert result == output_path
    assert calls == [
        [
            "ffmpeg",
            "-y",
            "-ss",
            "12.5",
            "-i",
            "input/live.mp4",
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(output_path),
        ]
    ]


def test_add_text_to_thumbnail_writes_jpg(tmp_path: Path) -> None:
    image_path = tmp_path / "frame.jpg"
    output_path = tmp_path / "thumbnail.jpg"
    Image.new("RGB", (640, 360), color=(40, 80, 120)).save(image_path)

    result = add_text_to_thumbnail(
        image_path=image_path,
        text="mano, não acredito nisso!",
        output_path=output_path,
    )

    assert result == output_path
    assert output_path.exists()
    assert Image.open(output_path).size == (640, 360)


def test_generate_thumbnails_from_edit_plan_creates_short_and_long_thumbnails(
    monkeypatch,
    tmp_path: Path,
) -> None:
    edit_plan_path = tmp_path / "cache" / "edit_plans" / "edit_plan.json"
    output_dir = tmp_path / "output" / "thumbnails"
    save_json(
        {
            "source_video": "input/live.mp4",
            "shorts": [
                {
                    "id": "short_01",
                    "start": 10.0,
                    "end": 20.0,
                    "title": "MANO, NÃO ACREDITO NISSO!",
                    "score": 0.9,
                }
            ],
            "long_videos": [
                {
                    "id": "video_01",
                    "title": "Melhores momentos da live",
                    "segments": [
                        {
                            "start": 100.0,
                            "end": 120.0,
                        }
                    ],
                }
            ],
        },
        edit_plan_path,
    )
    calls = []

    def fake_capture_frame(video_path, timestamp, output_path):
        calls.append((video_path, timestamp, Path(output_path).name))
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (640, 360), color=(20, 20, 20)).save(output_path)
        return Path(output_path)

    monkeypatch.setattr(thumbnail_generator, "OUTPUT_THUMBNAILS_DIR", output_dir)
    monkeypatch.setattr(thumbnail_generator, "capture_frame", fake_capture_frame)

    generated = generate_thumbnails_from_edit_plan(edit_plan_path)

    assert generated == [
        output_dir / "short_01.jpg",
        output_dir / "video_01.jpg",
    ]
    assert (output_dir / "short_01.jpg").exists()
    assert (output_dir / "video_01.jpg").exists()
    assert calls == [
        ("input/live.mp4", 15.0, "short_01_frame.jpg"),
        ("input/live.mp4", 110.0, "video_01_frame.jpg"),
    ]
