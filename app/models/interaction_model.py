# app/models/interaction_model.py

# 1. CORREÇÃO: Adicionamos 'Text' e 'DateTime' à importação
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class VideoLike(Base):
    __tablename__ = "video_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'video_id', name='_user_video_uc'),)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    # Esta linha agora funciona porque 'Text' foi importado
    text = Column(Text, nullable=False) 

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)

    owner = relationship("User", back_populates="comments")
    video = relationship("Video", back_populates="comments")