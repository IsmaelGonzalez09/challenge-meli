from pydantic import BaseModel

class PostScanSchema(BaseModel):
    connection_id: str