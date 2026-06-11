from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class TranscriptSegment(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    start: float = Field(ge=0)
    end: float = Field(ge=0)
    text: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_time_range(self) -> "TranscriptSegment":
        if self.end < self.start:
            raise ValueError("segment end must be greater than or equal to start")
        return self

    @field_validator("text")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return " ".join(value.split())


class Transcript(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    source_audio: str
    language: str | None = None
    duration: float | None = Field(default=None, ge=0)
    segments: list[TranscriptSegment]
