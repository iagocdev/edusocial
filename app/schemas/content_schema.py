# app/schemas/content_schema.py
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class VideoBase(BaseModel):
    title: str
    description: str | None = None
    url: HttpUrl # Pydantic vai validar se é uma URL válida

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True