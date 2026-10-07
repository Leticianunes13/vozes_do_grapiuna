import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "A variável de ambiente DATABASE_URL não foi encontrada no arquivo .env"
    )

# Cria a engine de conexão com o Neon
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Lida com o auto-suspend do Neon (reconecta se o banco dormir)
    pool_recycle=300,  # Recicla conexões antigas a cada 5 minutos
)

# Fabrica sessões do banco para cada requisição
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para a criação das tabelas (Models)
Base = declarative_base()


# Dependência do FastAPI: abre a conexão quando a rota precisa e fecha ao terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
