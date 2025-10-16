# app/crud/crud_user.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    # Pega a senha do usuário, gera um hash seguro
    hashed_password = get_password_hash(user.password)
    
    # Cria um novo objeto User do nosso modelo
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password # Salva a senha criptografada!
    )
    
    db.add(db_user)      # Adiciona o novo usuário à sessão do banco
    db.commit()          # Confirma a transação (salva no banco)
    db.refresh(db_user)  # Atualiza o objeto db_user com os dados do banco (como o ID)
    return db_user