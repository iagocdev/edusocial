# app/crud/crud_interaction.py
from sqlalchemy.orm import Session
from ..models import interaction_model
from ..schemas import interaction_schema

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

def create_comment(
    db: Session, 
    comment: interaction_schema.CommentCreate, 
    owner_id: int, 
    video_id: int
):
    db_comment = interaction_model.Comment(
        **comment.model_dump(),
        owner_id=owner_id,
        video_id=video_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_for_video(db: Session, video_id: int, skip: int = 0, limit: int = 20):
    return db.query(interaction_model.Comment).filter(
        interaction_model.Comment.video_id == video_id
    ).order_by(
        interaction_model.Comment.created_at.desc()
    ).options(
        joinedload(interaction_model.Comment.owner) # <-- Mágica! Carrega os dados do dono junto
    ).offset(skip).limit(limit).all()