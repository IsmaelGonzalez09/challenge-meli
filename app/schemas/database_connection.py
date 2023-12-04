from pydantic import BaseModel, SecretStr, Field

class DatabaseConnection(BaseModel):
    host: str
    port: int
    user: str
    password: SecretStr
    db_name: str = Field(..., alias='data_base')