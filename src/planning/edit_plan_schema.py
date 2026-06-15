from pydantic import BaseModel, Field


class EditAction(BaseModel):
    type: str
    start: float | None = None
    end: float | None = None
    time: float | None = None
    intensity: float | None = None
    target: str | None = None
    volume: float | None = None
    reason: str | None = None
    name: str | None = None
    style: str | None = None


class ShortPlan(BaseModel):
    id: str
    start: float = Field(ge=0)
    end: float = Field(ge=0)
    duration: float = Field(ge=0)
    score: float = Field(ge=0, le=1)
    title: str
    reason: str
    style: str = "highlight"
    actions: list[EditAction] = Field(default_factory=list)


class LongVideoSegment(BaseModel):
    start: float = Field(ge=0)
    end: float = Field(ge=0)
    duration: float = Field(ge=0)
    score: float = Field(ge=0, le=1)
    reason: str


class LongVideoPlan(BaseModel):
    id: str
    title: str
    duration_target: int
    theme: str
    segments: list[LongVideoSegment]
    actions: list[EditAction] = Field(default_factory=list)


class EditPlan(BaseModel):
    source_video: str
    shorts: list[ShortPlan]
    long_videos: list[LongVideoPlan]
