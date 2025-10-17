# app/crud/crud_quiz.py
from sqlalchemy.orm import Session
from typing import List
from ..models import quiz_model
from ..schemas import quiz_schema

# --- Funções para criar o Quiz ---

def create_quiz(db: Session, quiz: quiz_schema.QuizCreate, video_id: int):
    # 1. Cria o objeto Quiz (a "capa")
    db_quiz = quiz_model.Quiz(title=quiz.title, video_id=video_id)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    # 2. Itera sobre cada pergunta no schema e a cria
    for question_data in quiz.questions:
        create_question(db, question=question_data, quiz_id=db_quiz.id)

    db.refresh(db_quiz) # Atualiza o quiz com as perguntas criadas
    return db_quiz

def create_question(db: Session, question: quiz_schema.QuestionCreate, quiz_id: int):
    # 1. Cria o objeto Pergunta
    db_question = quiz_model.Question(text=question.text, quiz_id=quiz_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # 2. Itera sobre cada opção e a cria
    for option_data in question.options:
        create_option(db, option=option_data, question_id=db_question.id)

    return db_question

def create_option(db: Session, option: quiz_schema.OptionCreate, question_id: int):
    db_option = quiz_model.Option(**option.model_dump(), question_id=question_id)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option

# --- Funções para buscar o Quiz ---

def get_quiz_by_video_id(db: Session, video_id: int):
    # Retorna o quiz, já carregando suas perguntas e opções (eager loading)
    return db.query(quiz_model.Quiz).filter(quiz_model.Quiz.video_id == video_id).first()

# --- Funções para Resposta do Usuário ---

def get_option(db: Session, option_id: int):
    return db.query(quiz_model.Option).filter(quiz_model.Option.id == option_id).first()

def get_question(db: Session, question_id: int):
    return db.query(quiz_model.Question).filter(quiz_model.Question.id == question_id).first()

def submit_response(
    db: Session, 
    response: quiz_schema.UserResponseCreate, 
    user_id: int
):
    # 1. Cria o registro da resposta do usuário
    db_response = quiz_model.UserResponse(
        **response.model_dump(),
        user_id=user_id
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)

    # 2. Verifica se a resposta está correta
    selected_option = get_option(db, option_id=response.selected_option_id)

    # 3. Encontra qual era a opção correta para essa pergunta
    correct_option = db.query(quiz_model.Option).filter(
        quiz_model.Option.question_id == response.question_id,
        quiz_model.Option.is_correct == True
    ).first()

    return {
        "question_id": response.question_id,
        "selected_option_id": response.selected_option_id,
        "is_correct": selected_option.is_correct,
        "correct_option_id": correct_option.id
    }