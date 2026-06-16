from pydantic import BaseModel, Field


class EmotionSegment(BaseModel):
    start: float = Field(ge=0)
    end: float = Field(ge=0)
    text: str
    emotion: str
    emotion_score: float = Field(ge=0, le=1)
    audio_intensity: float = Field(ge=0, le=1)
    reasons: list[str]


class EmotionAnalysis(BaseModel):
    source_transcript: str
    source_audio: str
    segments: list[EmotionSegment]
