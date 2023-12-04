from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.post_scan_schema import PostScanSchema
from app.dependencies.db import get_db
from cryptography.fernet import Fernet
import json
import re
import uuid
import os

router = APIRouter()

# Carga la clave secreta de Fernet desde las variables de entorno
secret_key = os.getenv('SECRET_KEY')
cipher_suite = Fernet(secret_key)

# Función para descifrar la contraseña
def decrypt_password(encrypted_password: str) -> str:
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

# Diccionario de Clasificación
classification_rules = {
    "username": "USERNAME",
    "mail": "EMAIL_ADDRESS",
    "credit": "CREDIT_CARD_NUMBER"
}

# Funcion Regex para clasificar los datos
def classify_column(column_name):
    for pattern, classification in classification_rules.items():
        if re.search(pattern, column_name, re.IGNORECASE):
            return classification
    return "N/A"

# Endpoint Post scan
@router.post("/api/v1/database/scan/", tags=['Scan ID'])
def post_database_connection(connection_data: PostScanSchema, db: Session = Depends(get_db)):
    # Genera un nuevo UUID para esta ejecución del proceso
    process_id = str(uuid.uuid4())
    # Busca los datos de conexión en la base de datos utilizando el ID proporcionado
    connection_data = db.execute(text("SELECT * FROM connections WHERE id = :id"), {"id": connection_data.connection_id}).fetchone()
    if not connection_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID de conexión no encontrado")

    decrypted_password = decrypt_password(connection_data[4])
    classification_results = {
        "database_name": connection_data[5],
        "tables": {}
    }

    # Intenta conectarte con los datos descifrados para validarlos
    try:
        # Construye la URL de conexión con los datos descifrados y prueba la conexión
        database_url = f"mysql+mysqlconnector://{connection_data[3]}:{decrypted_password}@{connection_data[1]}:{connection_data[2]}/{connection_data[5]}"
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Consulta todas las tablas de la base de datos
            tables_result = conn.execute(text("SHOW TABLES;"))
            tables = [table[0] for table in tables_result]

            # Consulta los nombres de las tablas y columnas
            for table_name in tables:
                columns_result = conn.execute(text(f"SHOW COLUMNS FROM {table_name};"))
                classification_results["tables"][table_name] = []
                for column_info in columns_result:
                    column_name = column_info[0]
                    classification = classify_column(column_name)
                    classification_results["tables"][table_name].append({
                        "column_name": column_name,
                        "classification": classification                                        
                    })
            # Convierte los resultados de clasificación a un objeto JSON
            classification_json = json.dumps(classification_results)

            # Almacena el UUID y el objeto JSON en la tabla 'classification'
            db.execute(text("INSERT INTO persistent_data_db.classification (id, result) VALUES (:id, :result)"), {
                "id": process_id,
                "result": classification_json
            })
            db.commit()
            return {"message": "Classification Complete. Id: ", "process_id": process_id}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))