# app/crud/crud_content.py
from sqlalchemy.orm import Session
from ..models import content_model
from ..schemas import content_schema

def create_video(db: Session, video: content_schema.VideoCreate, owner_id: int):
    # Cria um novo objeto Video com os dados do schema e o ID do dono
    db_video = content_model.Video(
        **video.model_dump(), 
        owner_id=owner_id
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def get_videos(db: Session, skip: int = 0, limit: int = 100):
    # Retorna uma lista de vídeos, ordenados pelos mais recentes
    return db.query(content_model.Video).order_by(content_model.Video.created_at.desc()).offset(skip).limit(limit).all()


# app/crud/crud_content.py

def get_video(db: Session, video_id: int):
    # Busca um vídeo específico pelo seu ID
    return db.query(content_model.Video).filter(content_model.Video.id == video_id).first()