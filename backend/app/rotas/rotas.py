from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.infraestruturadb import get_db
from app.schemas import AutorResponse
from app.servicos import logica  # Importa o arquivo unico de servicos!

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.get("/", response_model=List[AutorResponse])
def listar_autores(db: Session = Depends(get_db)):
    return logica.listar_todos_autores(db)


@router.get("/{autor_id}", response_model=AutorResponse)
def obter_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = logica.buscar_autor_por_id(db, autor_id)
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado."
        )
    return autor
