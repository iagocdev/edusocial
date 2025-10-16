from fastapi import FastAPI
from app.core.database import engine
from app.models import user_model
from app.routers import user  # Importe o router do usuário

# Este comando cria as tabelas no banco de dados se elas não existirem
user_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduSocial API",
    description="A plataforma de ensino EAD que une educação, interação e monetização.",
    version="0.1.0"
)

# Inclua as rotas de usuário na aplicação principal
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do EduSocial! Acesse /docs para ver a documentação."}