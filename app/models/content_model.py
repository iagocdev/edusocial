# app/models/content_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(255), nullable=False)

    # Registra a data e hora da criação automaticamente
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # A MÁGICA ACONTECE AQUI: A CHAVE ESTRANGEIRA
    # Esta linha cria a ligação entre o vídeo e seu dono.
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Esta linha cria a relação no nível do SQLAlchemy
    owner = relationship("User")