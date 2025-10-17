from fastapi import FastAPI
from app.core.database import engine
from app.models import user_model, content_model # 1. Importamos o novo modelo
from app.routers import user, content # 2. Importamos o novo router

# 3. Dizemos ao SQLAlchemy para criar a tabela de vídeos também
user_model.Base.metadata.create_all(bind=engine)
content_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduSocial API",
    description="A plataforma de ensino EAD que une educação, interação e monetização.",
    version="0.1.0"
)

# 4. Incluímos as rotas de conteúdo na nossa API
app.include_router(user.router)
app.include_router(content.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do EduSocial! Acesse /docs para ver a documentação."}