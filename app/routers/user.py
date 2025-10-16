from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..crud import crud_user
from ..schemas.user_schema import User, UserCreate, Token
from ..core.database import get_db
from ..core import security
from ..models.user_model import User as UserModel # Importamos o modelo para type hint

router = APIRouter(
    tags=["Users & Authentication"]
)

# --- Endpoint de Cadastro (existente) ---
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    # ... (código existente, sem alterações) ...
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já está cadastrado."
        )
    return crud_user.create_user(db=db, user=user)

# --- Endpoint de Login (existente) ---
@router.post("/login/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # ... (código existente, sem alterações) ...
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- NOVA ROTA PROTEGIDA (A "Sala VIP") ---
@router.get("/users/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(security.get_current_user)):
    """
    Retorna os dados do usuário atualmente autenticado.
    """
    return current_user