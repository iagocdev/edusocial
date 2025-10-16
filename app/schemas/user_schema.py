# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from app.models.user_model import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

    # ESTA É A VALIDAÇÃO QUE IMPEDE O ERRO
    @field_validator('password')
    @classmethod
    def password_must_not_be_too_long(cls, v: str) -> str:
        # O bcrypt tem um limite de 72 bytes
        if len(v.encode('utf-8')) > 72:
            raise ValueError('A senha é muito longa e não pode exceder 72 bytes.')
        return v

class User(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None            