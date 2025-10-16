from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Cria o motor de conexão com o banco usando a URL do nosso .env
engine = create_engine(settings.DATABASE_URL)

# Cria uma sessão "fabricante"
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Uma classe base que nossos modelos de banco de dados irão herdar
Base = declarative_base()

# Função de dependência: para cada requisição, abre uma sessão e a fecha no final
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()