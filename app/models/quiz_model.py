# app/models/quiz_model.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

# 1. A "Capa" do Quiz
class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)

    # Chave estrangeira para o vídeo ao qual este quiz pertence
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False, unique=True)

    # Relações
    video = relationship("Video", back_populates="quiz")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")

# 2. As Perguntas do Quiz
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)

    # Chave estrangeira para o quiz ao qual esta pergunta pertence
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)

    # Relações
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

# 3. As Opções de cada Pergunta
class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)

    # Chave estrangeira para a pergunta à qual esta opção pertence
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    # Relação
    question = relationship("Question", back_populates="options")

# 4. O registro da Resposta do Usuário
class UserResponse(Base):
    __tablename__ = "user_responses"
    id = Column(Integer, primary_key=True, index=True)

    # Chave estrangeira para o usuário que respondeu
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Chave estrangeira para a pergunta que foi respondida
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    # Chave estrangeira para a opção que o usuário escolheu
    selected_option_id = Column(Integer, ForeignKey("options.id"), nullable=False)

    # Relações (opcional, mas bom para buscas)
    user = relationship("User")
    question = relationship("Question")
    selected_option = relationship("Option")