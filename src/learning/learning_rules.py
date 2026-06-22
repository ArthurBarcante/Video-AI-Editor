from src.learning.feedback_schema import LearningProfile


def apply_transcription_feedback_to_profile(
    profile: LearningProfile,
    replacements: dict[str, str],
) -> LearningProfile:
    preferred = profile.transcription.setdefault("preferred_replacements", {})
    preferred.update(replacements)
    return profile
