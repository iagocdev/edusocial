# app/routers/interaction.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List # <-- 1. IMPORTAR List

from ..crud import crud_interaction, crud_content
from ..schemas import interaction_schema
from ..models import user_model
from ..core import security
from ..core.database import get_db

router = APIRouter(
    tags=["Interactions"] # Tag para organizar na documentação
)

@router.post(
    "/videos/{video_id}/like", 
    response_model=interaction_schema.LikeResponse
)
def toggle_like_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(security.get_current_user)
):
    """
    Curte ou descurte um vídeo. (Endpoint protegido)

    - Se o vídeo não estiver curtido, ele será curtido.
    - Se o vídeo já estiver curtido, a curtida será removida.
    """
    # 1. Primeiro, verificar se o vídeo que está sendo curtido existe
    video = crud_content.get_video(db, video_id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")

    # 2. Verificar se o usuário logado (current_user) já curtiu este vídeo
    existing_like = crud_interaction.get_like(
        db, user_id=current_user.id, video_id=video_id
    )

    if existing_like:
        # 3. Se o like já existe, vamos REMOVER (descurtir)
        crud_interaction.delete_like(db, db_like=existing_like)
        return {"detail": "Curtida removida", "liked": False}
    else:
        # 4. Se o like não existe, vamos CRIAR (curtir)
        crud_interaction.create_like(db, user_id=current_user.id, video_id=video_id)
        return {"detail": "Vídeo curtido!", "liked": True}
    
@router.post(
    "/videos/{video_id}/comments", 
    response_model=interaction_schema.Comment
)
def create_new_comment(
    video_id: int,
    comment: interaction_schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(security.get_current_user)
):
    """
    Posta um novo comentário em um vídeo. (Endpoint protegido)
    """
    # 1. Verificar se o vídeo existe
    video = crud_content.get_video(db, video_id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")

    # 2. Criar o comentário
    return crud_interaction.create_comment(
        db=db, comment=comment, owner_id=current_user.id, video_id=video_id
    )

@router.get(
    "/videos/{video_id}/comments", 
    response_model=List[interaction_schema.Comment]
)
def read_video_comments(
    video_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Lista todos os comentários de um vídeo. (Endpoint público)
    """
    # 1. Verificar se o vídeo existe
    video = crud_content.get_video(db, video_id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")

    # 2. Buscar os comentários
    comments = crud_interaction.get_comments_for_video(
        db, video_id=video_id, skip=skip, limit=limit
    )
    return comments    