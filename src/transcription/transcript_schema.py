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


class TranscriptMetadata(BaseModel):
    execution_time_seconds: float
    audio_duration_seconds: float | None = None
    realtime_speed: float
    segment_count: int
    model: str
    device: str
    compute_type: str
    beam_size: int
    best_of: int
    vad_filter: bool
    word_timestamps: bool
    profile: str
    chunking_enabled: bool = False
    chunk_duration: int | None = None
    chunk_overlap: int | None = None
    chunk_count: int = 0
    chunks_reused_from_cache: int = 0
    chunk_metrics: list[dict] = Field(default_factory=list)


class Transcript(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    source_audio: str
    language: str | None = None
    duration: float | None = Field(default=None, ge=0)
    segments: list[TranscriptSegment]
    metadata: TranscriptMetadata
