from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(default="Untitled note", min_length=1, max_length=255)
    content: str = Field(default="", max_length=50_000)
    summary: str = Field(default="", max_length=2_000)
    tags: list[str] = Field(default_factory=list, max_length=10)


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, max_length=50_000)
    summary: str | None = Field(default=None, max_length=2_000)
    tags: list[str] | None = Field(default=None, max_length=10)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    summary: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class CaptureAssistRequest(BaseModel):
    content: str = Field(min_length=1, max_length=50_000)


class CaptureAssistResponse(BaseModel):
    title: str
    summary: str
    tags: list[str]
