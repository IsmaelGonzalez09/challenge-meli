from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Dinamic URL
PERSISTENT_DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('PERSISTENT_DB_USER')}:{os.getenv('PERSISTENT_DB_PASS')}@{os.getenv('PERSISTENT_DB_HOST')}:{os.getenv('PERSISTENT_DB_PORT')}/{os.getenv('PERSISTENT_DB_NAME')}"

# Function to connect to 'persistent_data_db'
def get_db():
    engine = create_engine(PERSISTENT_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()