from typing import Any, Literal

from pydantic import BaseModel, Field


class TranscriptionCorrection(BaseModel):
    type: Literal["transcription_error"] = "transcription_error"
    wrong: str
    correct: str
    context: str = ""
    apply_future: bool = True


class HighlightFeedback(BaseModel):
    type: Literal["highlight_feedback"] = "highlight_feedback"
    highlight_id: str
    decision: Literal["good", "bad"]
    reason: str = ""
    features: dict[str, Any] = Field(default_factory=dict)


class EditFeedback(BaseModel):
    type: Literal["edit_feedback"] = "edit_feedback"
    short_id: str
    problem: str | None = None
    correction: dict[str, Any] = Field(default_factory=dict)
    success: str | None = None
    repeat_pattern: bool = False


class FeedbackLog(BaseModel):
    items: list[TranscriptionCorrection | HighlightFeedback | EditFeedback] = Field(
        default_factory=list
    )


class CorrectionMemory(BaseModel):
    transcription_replacements: dict[str, str] = Field(default_factory=dict)


class LearningProfile(BaseModel):
    transcription: dict[str, Any] = Field(
        default_factory=lambda: {
            "preferred_replacements": {},
        }
    )
    highlights: dict[str, float] = Field(
        default_factory=lambda: {
            "keyword_weight": 0.15,
            "laugh_weight": 0.25,
            "emotion_weight": 0.30,
            "audio_intensity_weight": 0.20,
        }
    )
    editing: dict[str, Any] = Field(
        default_factory=lambda: {
            "default_zoom_intensity": 1.12,
            "max_sfx_per_short": 1,
            "short_padding_before": 2.0,
            "short_padding_after": 1.5,
        }
    )
    subtitles: dict[str, Any] = Field(
        default_factory=lambda: {
            "max_words_per_line": 4,
            "max_lines": 2,
            "style": "bold_clean",
        }
    )
    analytics_learning: dict[str, Any] = Field(
        default_factory=lambda: {
            "best_short_duration_range": [],
            "best_emotions": [],
            "preferred_title_patterns": [],
            "sfx_penalty_if_more_than": None,
            "zoom_preferred_intensity": None,
        }
    )
