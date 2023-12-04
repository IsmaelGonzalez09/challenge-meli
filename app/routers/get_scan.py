from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
import json

router = APIRouter()

@router.get("/api/v1/classification/{classification_id}", tags=['Classification'])
def get_classification_result(classification_id: str, db: Session = Depends(get_db)):
    # Busca el resultado en la tabla 'classification' utilizando el ID proporcionado
    classification_data = db.execute(text("SELECT result FROM classification WHERE id = :id"), {"id": classification_id}).fetchone()
    if not classification_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID de clasificación no encontrado")

    # Convierte el resultado de la base de datos (cadena JSON) a un objeto Python
    classification_result = json.loads(classification_data[0])

    return classification_result