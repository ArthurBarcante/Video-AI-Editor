from pathlib import Path

from src.config.paths import CACHE_EDIT_PLANS_DIR
from src.planning.edit_plan_schema import EditPlan
from src.planning.highlight_prioritizer import prioritize_highlights
from src.planning.long_video_planner import plan_long_videos
from src.planning.shorts_planner import plan_shorts
from src.utils.file_utils import format_project_path, load_json, save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def generate_edit_plan(
    source_video: str | Path,
    highlights_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
) -> Path:
    source_video = Path(source_video)
    highlights_path = Path(highlights_path)

    if output_path is None:
        output_path = CACHE_EDIT_PLANS_DIR / "edit_plan.json"

    output_path = Path(output_path)

    if output_path.exists() and not force:
        logger.info("Edit plan já existe em cache: %s", format_project_path(output_path))
        return output_path

    highlights = load_json(highlights_path)
    highlights = prioritize_highlights(highlights)

    shorts = plan_shorts(highlights)
    long_videos = plan_long_videos(highlights)

    edit_plan = EditPlan(
        source_video=format_project_path(source_video),
        shorts=shorts,
        long_videos=long_videos,
    )

    save_json(edit_plan.model_dump(), output_path)

    logger.info("Edit plan gerado: %s", format_project_path(output_path))
    logger.info("Shorts planejados: %s", len(shorts))
    logger.info("Vídeos longos planejados: %s", len(long_videos))

    return output_path
