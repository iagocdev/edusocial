# app/schemas/quiz_schema.py
from pydantic import BaseModel
from typing import List

# --- Schemas para Opções ---
class OptionBase(BaseModel):
    text: str
    is_correct: bool

class OptionCreate(OptionBase):
    pass

class Option(OptionBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas para Perguntas ---
class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    options: List[OptionCreate] # Ao criar uma pergunta, já passamos suas opções

class Question(QuestionBase):
    id: int
    options: List[Option] # Ao ler uma pergunta, lemos suas opções
    class Config:
        from_attributes = True

# --- Schemas para o Quiz ---
class QuizBase(BaseModel):
    title: str

class QuizCreate(QuizBase):
    questions: List[QuestionCreate] # Ao criar um quiz, já passamos suas perguntas

class Quiz(QuizBase):
    id: int
    video_id: int
    questions: List[Question] # Ao ler um quiz, lemos suas perguntas
    class Config:
        from_attributes = True

# --- Schemas para Resposta do Usuário ---
class UserResponseCreate(BaseModel):
    question_id: int
    selected_option_id: int

class UserResponseResult(BaseModel):
    question_id: int
    selected_option_id: int
    is_correct: bool
    correct_option_id: int