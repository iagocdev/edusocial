# app/schemas/interaction_schema.py
from pydantic import BaseModel
from datetime import datetime
from .user_schema import UserPublic # <-- 1. IMPORTAR UserPublic

class LikeResponse(BaseModel):
    detail: str
    liked: bool
    
class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    created_at: datetime
    owner: UserPublic # <-- Usamos o schema público aqui!

    class Config:
        from_attributes = True    