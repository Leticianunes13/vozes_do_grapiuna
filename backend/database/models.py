from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ARRAY
from sqlalchemy.sql import func
from database.infraestruturadb import Base


# 1. Tabela da Vitrine Literária (Submissões enviadas)
class Vitrine(Base):
    __tablename__ = "vitrine"

    id = Column(Integer, primary_key=True, index=True)
    nome_autor = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=False)
    titulo_texto = Column(String(150), nullable=True)
    texto = Column(Text, nullable=False)
    contato = Column(String(100), nullable=False)
    data_envio = Column(DateTime(timezone=True), server_default=func.now())
    # Status aceitos: 'pendente', 'publicado', 'arquivado'
    status_publicacao = Column(String(20), default="pendente")


# 2. Tabela de Autores Literários
class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nome_autor = Column(String(100), nullable=False)
    historia = Column(Text, nullable=False)
    obras = Column(ARRAY(String), nullable=False)
    resumo_obras = Column(Text, nullable=False)
    foto_url = Column(String(255), nullable=True)


# 3. Tabela do Mapa Afetivo (Leaflet.js)
class MapaAfetivo(Base):
    __tablename__ = "mapa_afetivo"

    id = Column(Integer, primary_key=True, index=True)
    local = Column(String(100), nullable=False)
    texto_informativo = Column(Text, nullable=False)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    foto_url = Column(String(255), nullable=True)
