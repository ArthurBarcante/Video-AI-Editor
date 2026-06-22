from typing import Any

from pydantic import BaseModel, Field


class VideoMetrics(BaseModel):
    video_id: str
    platform: str
    title: str = ""
    duration: float = Field(ge=0)
    views: int = Field(ge=0)
    likes: int = Field(ge=0)
    comments: int = Field(ge=0)
    shares: int = Field(ge=0)
    watch_time_seconds: float = Field(default=0, ge=0)
    average_view_duration: float = Field(default=0, ge=0)
    retention_rate: float = Field(default=0, ge=0)
    click_through_rate: float = Field(default=0, ge=0)
    published_at: str | None = None
    source_features: dict[str, Any] = Field(default_factory=dict)


class VideoMetricsDataset(BaseModel):
    items: list[VideoMetrics] = Field(default_factory=list)


class PerformancePattern(BaseModel):
    name: str
    value: Any
    reason: str
    sample_size: int


class PerformanceReport(BaseModel):
    total_videos: int
    average_retention_rate: float
    average_click_through_rate: float
    patterns: list[PerformancePattern] = Field(default_factory=list)
