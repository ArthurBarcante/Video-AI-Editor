from pathlib import Path

from src.config.paths import CACHE_CONTEXT_DIR
from src.context.context_schema import ContextAnalysis, ContextBlock
from src.context.semantic_analyzer import (
    calculate_context_importance,
    extract_keywords,
    infer_topic,
)
from src.context.topic_grouper import group_segments_into_blocks
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.utils.file_utils import format_project_path, load_json, save_json
from src.utils.logger import get_logger

logger = get_logger(__name__)


def analyze_context(
    transcript_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
) -> Path:
    transcript_path = Path(transcript_path)

    if output_path is None:
        output_path = CACHE_CONTEXT_DIR / "context.json"

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        logger.info("Contexto já existe em cache: %s", format_project_path(output_path))
        return output_path

    transcript = load_json(transcript_path)
    segments = transcript.get("segments", [])

    raw_blocks = group_segments_into_blocks(segments)

    blocks = []

    for index, block in enumerate(raw_blocks, start=1):
        text = " ".join(block["texts"]).strip()

        keywords = extract_keywords(text)
        topic = infer_topic(text, keywords)
        importance_score, reasons = calculate_context_importance(
            text=text,
            keywords=keywords,
            topic=topic,
        )

        context_block = ContextBlock(
            id=f"context_{index:03}",
            start=block["start"],
            end=block["end"],
            duration=round(block["end"] - block["start"], 2),
            text=text,
            keywords=keywords,
            topic=topic,
            importance_score=importance_score,
            reasons=reasons,
        )

        blocks.append(context_block)

    analysis = ContextAnalysis(
        source_transcript=format_project_path(transcript_path),
        blocks=blocks,
    )

    save_json(analysis.model_dump(), output_path)

    logger.info("Blocos de contexto gerados: %s", len(blocks))
    logger.info("Contexto salvo em: %s", format_project_path(output_path))

    return output_path
