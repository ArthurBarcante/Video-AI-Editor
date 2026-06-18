from pydantic import BaseModel, Field


class PublishTarget(BaseModel):
    platform: str
    video_path: str
    title: str
    description: str = ""
    tags: list[str] = Field(default_factory=list)
    scheduled_at: str | None = None
    privacy_status: str = "private"
    status: str = "pending"


class PublishPlan(BaseModel):
    items: list[PublishTarget] = Field(default_factory=list)
