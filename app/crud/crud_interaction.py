# app/crud/crud_interaction.py
from sqlalchemy.orm import Session
from ..models import interaction_model

def get_like(db: Session, user_id: int, video_id: int):
    """
    Verifica se um usuário específico já curtiu um vídeo específico.
    """
    return db.query(interaction_model.VideoLike).filter(
        interaction_model.VideoLike.user_id == user_id,
        interaction_model.VideoLike.video_id == video_id
    ).first()

def create_like(db: Session, user_id: int, video_id: int):
    """
    Registra uma nova curtida no banco.
    """
    db_like = interaction_model.VideoLike(user_id=user_id, video_id=video_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def delete_like(db: Session, db_like: interaction_model.VideoLike):
    """
    Remove uma curtida do banco.
    """
    db.delete(db_like)
    db.commit()
    return db_like