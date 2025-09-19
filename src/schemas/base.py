from pydantic import BaseModel
from typing import TypeVar, Optional
from datetime import datetime

T = TypeVar('T')

class ResponseSchema(BaseModel):
    """Esquema base para respuestas API"""
    success: bool = True
    message: str = "Operación exitosa"
    data: Optional[T] = None

class DateTimeSchema(BaseModel):
    """Esquema para timestamps"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
