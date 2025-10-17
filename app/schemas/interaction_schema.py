# app/schemas/interaction_schema.py
from pydantic import BaseModel

class LikeResponse(BaseModel):
    detail: str
    liked: bool