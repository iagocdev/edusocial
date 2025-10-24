# main.py (Versão Final com CORS)

from fastapi import FastAPI
# 1. IMPORTAR O MIDDLEWARE DE CORS
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine
from app.models import user_model, content_model, interaction_model, quiz_model
from app.routers import user, content, interaction, quiz

# Cria as tabelas (sem mudança)
user_model.Base.metadata.create_all(bind=engine)
content_model.Base.metadata.create_all(bind=engine)
interaction_model.Base.metadata.create_all(bind=engine)
quiz_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduSocial API",
    description="A plataforma de ensino EAD que une educação, interação e monetização.",
    version="0.1.0"
)

# 2. DEFINIR AS ORIGENS PERMITIDAS
#    Usamos ["*"] (wildcard) para permitir que QUALQUER
#    origem se conecte. Perfeito para desenvolvimento.
origins = ["*"]

# 3. ADICIONAR O MIDDLEWARE AO 'app'
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# Inclui os routers (sem mudança)
app.include_router(user.router)
app.include_router(content.router)
app.include_router(interaction.router)
app.include_router(quiz.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do EduSocial! Acesse /docs para ver a documentação."}