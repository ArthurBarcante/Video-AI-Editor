from pydantic import BaseModel, Field


class TitleSuggestion(BaseModel):
    target_id: str
    target_type: str
    title: str
    score: float = Field(ge=0, le=1)
    reason: str


class TitleAnalysis(BaseModel):
    suggestions: list[TitleSuggestion]
