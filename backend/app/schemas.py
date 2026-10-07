from pydantic import BaseModel
from typing import List, Optional

# ==========================================
# SCHEMAS DO ACERVO DE AUTORES
# ==========================================


class AutorResponse(BaseModel):
    id: int
    nome_autor: str
    historia: str
    obras: List[str]  # Ex: ["Cacau", "Gabriela, Cravo e Canela"]
    resumo_obras: Optional[str] = None  # Resumo/sinopse que fica ao lado das capas
    foto_url: Optional[str] = None

    class Config:
        from_attributes = True


# ==========================================
# SCHEMAS DO SISTEMA (Vitrine / Mapa)
# ==========================================
