from datetime import datetime, timedelta
from typing import Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import settings
from ..crud import crud_user
from ..schemas.user_schema import TokenData
from ..core.database import get_db

# --- Lógica de Senha (existente) ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Lógica de Token (existente) ---
# ... (as funções verify_password, get_password_hash, create_access_token continuam aqui) ...
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# --- NOVA LÓGICA DE VALIDAÇÃO (O "Segurança") ---

# Esta linha cria um "esquema" que diz: "Para se autenticar,
# o usuário deve enviar um header 'Authorization' com 'Bearer ' seguido do token."
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Tenta decodificar o token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # Busca o usuário no banco de dados com o e-mail extraído do token
    user = crud_user.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    # Retorna o objeto do usuário completo
    return user