from pathlib import Path

from src.analytics.performance_analyzer import LEARNED_PATTERNS_PATH
from src.learning.correction_memory import (
    LEARNING_PROFILE_PATH,
    load_learning_profile,
    save_learning_profile,
)
from src.utils.file_utils import load_json
from src.utils.logger import get_logger


logger = get_logger(__name__)


def apply_metrics_to_learning_profile(
    learned_patterns_path: str | Path = LEARNED_PATTERNS_PATH,
    profile_path: str | Path = LEARNING_PROFILE_PATH,
) -> Path:
    learned_patterns_path = Path(learned_patterns_path)

    if not learned_patterns_path.exists():
        raise FileNotFoundError(f"Padrões de analytics não encontrados: {learned_patterns_path}")

    profile = load_learning_profile(profile_path)
    learned_patterns = load_json(learned_patterns_path)
    profile.analytics_learning.update(
        {
            key: value
            for key, value in learned_patterns.items()
            if value not in (None, [], {})
        }
    )
    output_path = save_learning_profile(profile, profile_path)

    logger.info("Learning profile atualizado com métricas reais: %s", output_path)

    return output_path
