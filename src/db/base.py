from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any, Dict


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
    

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)


    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario, excluyendo campos internos"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in ["deleted_at"]
        }
    
    def __repr__(self) -> str:
        """Representación del modelo para debugging"""
        params = ', '.join(
            f"{key}={value}"
            for key, value in self.to_dict().items()
        )
        return f"<{self.__class__.__name__}({params})>"