from pydantic import BaseModel, Field


class ContextBlock(BaseModel):
    id: str
    start: float = Field(ge=0)
    end: float = Field(ge=0)
    duration: float = Field(ge=0)
    text: str
    keywords: list[str]
    topic: str
    importance_score: float = Field(ge=0, le=1)
    reasons: list[str]


class ContextAnalysis(BaseModel):
    source_transcript: str
    blocks: list[ContextBlock]
