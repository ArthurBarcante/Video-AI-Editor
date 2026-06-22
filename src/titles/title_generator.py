from pathlib import Path

from src.config.paths import CACHE_TITLES_DIR
from src.rendering.ffmpeg_utils import ensure_safe_project_output_path
from src.titles.title_rules import generate_title_variants, score_title
from src.titles.title_schema import TitleAnalysis, TitleSuggestion
from src.utils.cache_metadata import is_cache_valid, save_cache_metadata
from src.utils.file_utils import format_project_path, load_json, save_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def _load_optional_blocks(path: str | Path | None, key: str) -> list[dict]:
    if path is None:
        return []

    data = load_json(path)
    return data.get(key, [])


def generate_titles(
    edit_plan_path: str | Path,
    output_path: str | Path | None = None,
    force: bool = False,
    context_path: str | Path | None = None,
    emotions_path: str | Path | None = None,
) -> Path:
    edit_plan_path = Path(edit_plan_path)

    if output_path is None:
        output_path = CACHE_TITLES_DIR / "titles.json"

    output_path = Path(output_path)
    ensure_safe_project_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cache_sources = [
        edit_plan_path,
        *([Path(context_path)] if context_path else []),
        *([Path(emotions_path)] if emotions_path else []),
    ]

    if output_path.exists() and not force and is_cache_valid(output_path, cache_sources):
        logger.info("Títulos já existem em cache: %s", format_project_path(output_path))
        return output_path

    edit_plan = load_json(edit_plan_path)
    context_blocks = _load_optional_blocks(context_path, "blocks")
    emotion_segments = _load_optional_blocks(emotions_path, "segments")

    suggestions = []

    for short in edit_plan.get("shorts", []):
        variants = generate_title_variants(
            text=short.get("title", ""),
            style=short.get("style", "highlight"),
        )

        for title in variants:
            suggestions.append(
                TitleSuggestion(
                    target_id=short["id"],
                    target_type="short",
                    title=title,
                    score=score_title(title),
                    reason=f"gerado a partir do estilo {short.get('style')}",
                )
            )

    for video in edit_plan.get("long_videos", []):
        long_titles = [
            "OS MELHORES MOMENTOS DA LIVE",
            "A LIVE MAIS CAÓTICA DO CANAL",
            "MELHORES MOMENTOS COM A GALERA",
        ]

        for title in long_titles:
            suggestions.append(
                TitleSuggestion(
                    target_id=video["id"],
                    target_type="long_video",
                    title=title,
                    score=score_title(title),
                    reason="título gerado para vídeo longo",
                )
            )

    suggestions = sorted(
        suggestions,
        key=lambda item: item.score,
        reverse=True,
    )

    analysis = TitleAnalysis(suggestions=suggestions)

    save_json(analysis.model_dump(), output_path)
    save_cache_metadata(output_path, cache_sources)

    logger.info("Sugestões de títulos geradas: %s", len(suggestions))
    logger.info("Títulos salvos em: %s", format_project_path(output_path))
    logger.debug(
        "Títulos gerados com contexto=%s e emoções=%s",
        len(context_blocks),
        len(emotion_segments),
    )

    return output_path
