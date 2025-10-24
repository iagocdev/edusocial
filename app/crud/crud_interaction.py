# app/crud/crud_interaction.py

# --- A CORREÇÃO ESTÁ AQUI ---
# Nós importamos 'joinedload' da 'sqlalchemy.orm'
from sqlalchemy.orm import Session, joinedload 

from ..models import interaction_model
from ..schemas import interaction_schema

# --- FUNÇÕES DE LIKE (JÁ EXISTENTES) ---
def get_like(db: Session, user_id: int, video_id: int):
    return db.query(interaction_model.VideoLike).filter(
        interaction_model.VideoLike.user_id == user_id,
        interaction_model.VideoLike.video_id == video_id
    ).first()

def create_like(db: Session, user_id: int, video_id: int):
    db_like = interaction_model.VideoLike(user_id=user_id, video_id=video_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def delete_like(db: Session, db_like: interaction_model.VideoLike):
    db.delete(db_like)
    db.commit()
    return db_like

# --- FUNÇÕES DE COMENTÁRIO (JÁ EXISTENTES) ---
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
        # Esta linha agora funciona porque 'joinedload' foi importado
        joinedload(interaction_model.Comment.owner) 
    ).offset(skip).limit(limit).all()