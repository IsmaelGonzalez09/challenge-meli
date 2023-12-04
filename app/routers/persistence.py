from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.dependencies.db import get_db
from app.schemas.database_connection import DatabaseConnection
import uuid
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

# Key Encript
secret_key = os.getenv('SECRET_KEY')
cipher_suite = Fernet(secret_key)

# Función para cifrar la contraseña
def encrypt_password(password: str) -> str:
    return cipher_suite.encrypt(password.encode()).decode()

# Función para almacenar los datos de conexión
def store_connection_data(db: Session, host: str, port: int, user: str, password: str, db_name: str) -> str:
    encrypted_password = encrypt_password(password)
    unique_id = str(uuid.uuid4())
    db.execute(text("INSERT INTO connections (id, host, port, user, password, data_base) VALUES (:id, :host, :port, :user, :password, :data_base)"), {
        "id": unique_id,
        "host": host,
        "port": port,
        "user": user,
        "password": encrypted_password,
        "data_base": db_name
    })
    db.commit()
    return unique_id

@router.post("/api/v1/database", tags=['Persistence'], status_code=status.HTTP_201_CREATED)
def persist_database_connection(response: Response, connection_data: DatabaseConnection, db: Session = Depends(get_db)):
    # Intenta conectarte con los datos proporcionados para validarlos
    try:
        # Construye la URL de conexión con los datos del request body
        temp_database_url = f"mysql+mysqlconnector://{connection_data.user}:{connection_data.password.get_secret_value()}@{connection_data.host}:{connection_data.port}/{connection_data.db_name}"
        # Crea un motor temporal y prueba la conexión
        temp_engine = create_engine(temp_database_url)
        with temp_engine.connect() as temp_conn:
            # Busca todas las bases de datos disponibles
            result = temp_conn.execute(text("SHOW TABLES;"))
            [table[0] for table in result]

    except SQLAlchemyError as e:
        # Si hay un error de conexión, devuelve el código de estado correspondiente
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    try:
        # Si la conexión es exitosa, almacena los datos de conexión utilizando la función 'store_connection_data'
        unique_id = store_connection_data(
            db,
            connection_data.host,
            connection_data.port,
            connection_data.user,
            connection_data.password.get_secret_value(),
            connection_data.db_name
        )
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Connection data saved.", "Unique_id": unique_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))