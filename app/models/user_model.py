# app/models/user_model.py
from sqlalchemy import Column, Integer, String, Enum
from ..core.database import Base # Precisaremos criar este arquivo de conexão
import enum

class UserRole(str, enum.Enum):
    ALUNO = "aluno"
    CRIADOR = "criador"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.ALUNO)