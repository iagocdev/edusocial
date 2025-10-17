# app/models/user_model.py

# 1. CORREÇÃO: Importamos 'Enum' do SQLAlchemy com um "apelido"
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
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

    # 2. CORREÇÃO: Usamos o "apelido" que importamos
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.ALUNO)

    # Esta linha (que adicionamos no passo anterior) está correta
    comments = relationship("Comment", back_populates="owner")