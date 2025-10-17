# app/routers/quiz.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..crud import crud_quiz, crud_content
from ..schemas import quiz_schema
from ..models import user_model
from ..core import security
from ..core.database import get_db

router = APIRouter(
    tags=["Quizzes"]
)

@router.post(
    "/videos/{video_id}/quiz", 
    response_model=quiz_schema.Quiz
)
def create_quiz_for_video(
    video_id: int,
    quiz: quiz_schema.QuizCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(security.get_current_user)
):
    """
    Cria um novo quiz para um vídeo. (Endpoint protegido)

    - Apenas o dono do vídeo pode criar um quiz.
    - Um vídeo só pode ter um quiz.
    """
    # 1. Verificar se o vídeo existe
    video = crud_content.get_video(db, video_id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")

    # 2. Verificar se o usuário logado é o dono do vídeo
    if video.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado: Você não é o dono deste vídeo")

    # 3. Verificar se o vídeo já não tem um quiz
    if video.quiz:
        raise HTTPException(status_code=400, detail="Este vídeo já possui um quiz")

    # 4. Criar o quiz
    return crud_quiz.create_quiz(db=db, quiz=quiz, video_id=video_id)

@router.get(
    "/videos/{video_id}/quiz", 
    response_model=quiz_schema.Quiz
)
def read_video_quiz(video_id: int, db: Session = Depends(get_db)):
    """
    Pega o quiz associado a um vídeo. (Endpoint público)
    """
    quiz = crud_quiz.get_quiz_by_video_id(db, video_id=video_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz não encontrado para este vídeo")
    return quiz

@router.post(
    "/quiz/submit", 
    response_model=List[quiz_schema.UserResponseResult]
)
def submit_quiz_responses(
    responses: List[quiz_schema.UserResponseCreate],
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(security.get_current_user)
):
    """
    Submete as respostas de um usuário para um quiz. (Endpoint protegido)
    Recebe uma *lista* de respostas e retorna uma *lista* de resultados.
    """
    results = []
    for response in responses:
        # 1. Validar se a pergunta e a opção existem
        question = crud_quiz.get_question(db, question_id=response.question_id)
        option = crud_quiz.get_option(db, option_id=response.selected_option_id)

        if not question or not option:
            raise HTTPException(status_code=404, detail=f"Pergunta ou Opção ID {response.question_id}/{response.selected_option_id} não encontrada")

        # 2. Validar se a opção pertence à pergunta
        if option.question_id != question.id:
            raise HTTPException(status_code=400, detail=f"Opção {option.id} não pertence à Pergunta {question.id}")

        # 3. Submeter a resposta e obter o resultado
        result = crud_quiz.submit_response(db, response=response, user_id=current_user.id)
        results.append(result)

    return results