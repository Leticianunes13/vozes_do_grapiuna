from sqlalchemy.orm import Session
from database.models import Autor

# ==========================================
# SERVIÇOS DO ACERVO DE AUTORES
# ==========================================


def listar_todos_autores(db: Session):
    """
    Busca todos os autores cadastrados no Neon PostgreSQL.
    O SQLAlchemy traz automaticamente todos os campos da tabela
    (id, nome_autor, historia, obras, resumo_obras, foto_url).
    """
    return db.query(Autor).all()


def buscar_autor_por_id(db: Session, autor_id: int):
    """
    Busca um único autor pelo seu ID.
    """
    return db.query(Autor).filter(Autor.id == autor_id).first()
