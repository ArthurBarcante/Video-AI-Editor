from pydantic import BaseModel, Field


class Highlight(BaseModel):
    start: float = Field(ge=0)
    end: float = Field(ge=0)
    text: str
    score: float = Field(ge=0, le=1)
    reasons: list[str]