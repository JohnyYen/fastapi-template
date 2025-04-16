# app/core/exceptions.py
from fastapi import HTTPException, status
from typing import Optional, Any

class AppException(HTTPException):
    """Clase base para todas las excepciones personalizadas"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.detail = detail
        self.status_code = status_code

class NotFoundException(AppException):
    """Excepción cuando no se encuentra un recurso"""
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class DuplicateEntryException(AppException):
    """Excepción cuando se intenta crear un recurso que ya existe"""
    def __init__(self, detail: str = "El recurso ya existe"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class InvalidCredentialsException(AppException):
    """Excepción cuando las credenciales son inválidas"""
    def __init__(self, detail: str = "Credenciales inválidas"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class UnauthorizedException(AppException):
    """Excepción cuando el usuario no tiene permisos"""
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class DatabaseException(AppException):
    """Excepción para errores de base de datos"""
    def __init__(self, detail: str = "Error en la base de datos"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )