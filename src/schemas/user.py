from pydantic import BaseModel, EmailStr, Field, validator, root_validator
import re
from typing import Optional
from .base import ResponseSchema, DateTimeSchema

# ------------------------
# Esquemas de Autenticación
# ------------------------

class UserLogin(BaseModel):
    """Esquema para inicio de sesión"""
    username: str = Field(..., example="User")
    email: EmailStr = Field(..., example="usuario@example.com")
    password: str = Field(..., min_length=8, example="Password123!")

class UserLoginResponse(BaseModel):
    """Respuesta de autenticación exitosa"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: 'UserResponse'

# ------------------------
# Esquemas de Operaciones CRUD
# ------------------------

class UserBase(BaseModel):
    """Campos base compartidos"""
    username: str = Field(..., example="usuario")
    email: EmailStr = Field(..., example="usuario@example.com")

class UserCreate(UserBase):
    """Esquema para creación de usuario"""
    password: str = Field(..., min_length=8, example="Password123!")
    role_id: Optional[int] = Field(None, gt=0, example=1)

    @validator('password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una mayúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe contener al menos una minúscula")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe contener al menos un número")
        return v

class UserUpdate(BaseModel):
    """Esquema para actualización de usuario"""
    email: Optional[EmailStr] = Field(None, example="nuevo@example.com")

    @validator('email')
    def email_not_empty(cls, v):
        if v == "":
            raise ValueError("El email no puede estar vacío")
        return v

class UserChangePassword(BaseModel):
    """Esquema para cambio de contraseña"""
    current_password: str = Field(..., example="Current123!")
    new_password: str = Field(..., min_length=8, example="NewPassword123!")

    @validator('new_password')
    def validate_new_password(cls, v):
        return UserCreate.validate_password_strength(cls, v)

    @root_validator
    def validate_password_change(cls, values):
        if values.get('current_password') == values.get('new_password'):
            raise ValueError("La nueva contraseña debe ser diferente a la actual")
        return values

# ------------------------
# Esquemas de Respuesta
# ------------------------

class UserRoleResponse(BaseModel):
    """Esquema para respuesta de rol"""
    id: int
    name: str

class UserResponse(UserBase, DateTimeSchema):
    """Esquema para respuesta de usuario"""
    id: int
    is_active: bool = True
    role: Optional[UserRoleResponse] = None

    class Config:
        from_attributes = True

class UserListResponse(ResponseSchema):
    """Respuesta para listado de usuarios"""
    data: list[UserResponse]

class SingleUserResponse(ResponseSchema):
    """Respuesta para un solo usuario"""
    data: UserResponse

# ------------------------
# Validaciones Adicionales
# ------------------------

def validate_email_allowed(email: str) -> str:
    """Valida dominios de email permitidos"""
    blocked_domains = ["example.com"]  # Dominios no permitidos
    domain = email.split('@')[-1]
    if domain in blocked_domains:
        raise ValueError(f"El dominio {domain} no está permitido")
    return email

# Actualizar referencias circulares
UserLoginResponse.update_forward_refs()