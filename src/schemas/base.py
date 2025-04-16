from pydantic import BaseModel
from typing import TypeVar, Optional

T = TypeVar('T')

class ResponseSchema(BaseModel):
    """Esquema base para respuestas API"""
    success: bool = True
    message: str = "Operación exitosa"
    data: Optional[T] = None
