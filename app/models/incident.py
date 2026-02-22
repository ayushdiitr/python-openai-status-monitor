from pydantic import BaseModel

from datetime import datetime

class Incident(BaseModel):
    id: str
    provider: str
    status: str
    product: str
    metadata: object
    message: str
    created_at: datetime