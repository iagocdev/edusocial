# app/models/interaction_model.py
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from ..core.database import Base

class VideoLike(Base):
    __tablename__ = "video_likes"

    id = Column(Integer, primary_key=True, index=True)

    # Chave estrangeira para o usuário que curtiu
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Chave estrangeira para o vídeo que foi curtido
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)

    # A REGRA DE OURO:
    # Garante que a combinação de (user_id, video_id) seja ÚNICA.
    # Impede que o mesmo usuário curta o mesmo vídeo várias vezes.
    __table_args__ = (UniqueConstraint('user_id', 'video_id', name='_user_video_uc'),)