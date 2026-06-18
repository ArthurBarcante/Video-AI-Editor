from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from src.config.paths import OUTPUT_THUMBNAILS_DIR
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.thumbnails.frame_capture import capture_frame
from src.thumbnails.thumbnail_selector import select_thumbnail_timestamp
from src.utils.file_utils import format_project_path, load_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def _load_thumbnail_font(font_size: int) -> ImageFont.ImageFont:
    for font_name in [
        "DejaVuSans-Bold.ttf",
        "Arial.ttf",
    ]:
        try:
            return ImageFont.truetype(font_name, font_size)
        except OSError:
            continue

    return ImageFont.load_default()


def add_text_to_thumbnail(
    image_path: str | Path,
    text: str,
    output_path: str | Path,
) -> Path:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    width, height = image.size
    font_size = max(42, width // 18)
    font = _load_thumbnail_font(font_size)

    text = text.strip().replace("\n", " ").upper()

    max_chars = 32
    if len(text) > max_chars:
        text = text[: max_chars - 3] + "..."

    x = int(width * 0.05)
    y = int(height * 0.72)
    box_padding = 24

    bbox = draw.textbbox((x, y), text, font=font)

    draw.rectangle(
        [
            bbox[0] - box_padding,
            bbox[1] - box_padding,
            bbox[2] + box_padding,
            bbox[3] + box_padding,
        ],
        fill=(0, 0, 0),
    )

    draw.text(
        (x, y),
        text,
        font=font,
        fill=(255, 255, 255),
    )

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, quality=95)

    return output_path


def generate_thumbnails_from_edit_plan(
    edit_plan_path: str | Path,
    force: bool = False,
) -> list[Path]:
    edit_plan = load_json(edit_plan_path)

    source_video = edit_plan["source_video"]
    generated = []

    for short in edit_plan.get("shorts", []):
        output_path = OUTPUT_THUMBNAILS_DIR / f"{short['id']}.jpg"
        frame_path = OUTPUT_THUMBNAILS_DIR / "frames" / f"{short['id']}_frame.jpg"

        if output_path.exists() and not force:
            logger.info("Thumbnail já existe: %s", format_project_path(output_path))
            generated.append(output_path)
            continue

        timestamp = select_thumbnail_timestamp(short)

        capture_frame(
            video_path=source_video,
            timestamp=timestamp,
            output_path=frame_path,
        )

        thumbnail_path = add_text_to_thumbnail(
            image_path=frame_path,
            text=short.get("title", "MELHOR MOMENTO"),
            output_path=output_path,
        )

        generated.append(thumbnail_path)
        logger.info("Thumbnail gerada: %s", format_project_path(thumbnail_path))

    for video in edit_plan.get("long_videos", []):
        if not video.get("segments"):
            continue

        first_segment = video["segments"][0]
        output_path = OUTPUT_THUMBNAILS_DIR / f"{video['id']}.jpg"
        frame_path = OUTPUT_THUMBNAILS_DIR / "frames" / f"{video['id']}_frame.jpg"

        if output_path.exists() and not force:
            logger.info("Thumbnail já existe: %s", format_project_path(output_path))
            generated.append(output_path)
            continue

        timestamp = select_thumbnail_timestamp(first_segment)

        capture_frame(
            video_path=source_video,
            timestamp=timestamp,
            output_path=frame_path,
        )

        thumbnail_path = add_text_to_thumbnail(
            image_path=frame_path,
            text=video.get("title", "MELHORES MOMENTOS"),
            output_path=output_path,
        )

        generated.append(thumbnail_path)
        logger.info("Thumbnail gerada: %s", format_project_path(thumbnail_path))

    return generated
