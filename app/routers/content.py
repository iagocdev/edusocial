# app/routers/content.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# --- CORREÇÃO NAS IMPORTAÇÕES ---
# Em vez de 'from .. import crud, schemas, models',
# nós importamos os módulos específicos que precisamos:
from ..crud import crud_content
from ..schemas import content_schema
from ..models import user_model
from ..core import security
from ..core.database import get_db

router = APIRouter(
    prefix="/videos",
    tags=["Content"]
)

# --- CORREÇÃO NO USO ---
# Agora usamos os módulos importados diretamente
@router.post("/", response_model=content_schema.Video)
def create_new_video(
    video: content_schema.VideoCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(security.get_current_user)
):
    """
    Cria um novo vídeo. Apenas para usuários autenticados.
    """
    return crud_content.create_video(db=db, video=video, owner_id=current_user.id)

# --- CORREÇÃO NO USO ---
@router.get("/", response_model=List[content_schema.Video])
def read_videos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna uma lista de vídeos (o feed). Rota pública.
    """
    videos = crud_content.get_videos(db, skip=skip, limit=limit)
    return videos