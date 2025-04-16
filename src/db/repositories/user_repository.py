# app/db/repositories/user_repository.py
from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.core.security import get_password_hash, verify_password
from src.core.exceptions import (
    NotFoundException,
    DuplicateEntryException,
    InvalidCredentialsException
)


class UserRepository:
    """Repositorio para operaciones de base de datos relacionadas con usuarios.
    
    Provee métodos CRUD con validaciones y manejo de errores específicos.
    Implementa soft delete y actualización parcial de campos.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int, include_deleted: bool = False) -> Optional[User]:
        """Obtiene un usuario por ID.
        
        Args:
            user_id: ID del usuario a buscar
            include_deleted: Si True, incluye usuarios marcados como eliminados
            
        Returns:
            User: Instancia del modelo User si se encuentra, None en caso contrario
        """
        query = select(User).where(User.id == user_id)
        if not include_deleted:
            query = query.where(User.deleted_at.is_(None))
            
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> List[User]:
        """Obtiene todos los usuarios con paginación.
        
        Args:
            skip: Número de registros a saltar (para paginación)
            limit: Máximo número de registros a devolver
            include_deleted: Si True, incluye usuarios marcados como eliminados
            
        Returns:
            List[User]: Lista de usuarios
        """
        query = select(User).offset(skip).limit(limit)
        if not include_deleted:
            query = query.where(User.deleted_at.is_(None))
            
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_email(self, email: str, include_deleted: bool = False) -> Optional[User]:
        """Busca un usuario por email.
        
        Args:
            email: Email del usuario a buscar
            include_deleted: Si True, incluye usuarios marcados como eliminados
            
        Returns:
            User: Instancia del modelo User si se encuentra, None en caso contrario
        """
        query = select(User).where(User.email == email)
        if not include_deleted:
            query = query.where(User.deleted_at.is_(None))
            
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str, include_deleted: bool = False) -> Optional[User]:
        """Busca un usuario por nombre de usuario.
        
        Args:
            username: Nombre de usuario a buscar
            include_deleted: Si True, incluye usuarios marcados como eliminados
            
        Returns:
            User: Instancia del modelo User si se encuentra, None en caso contrario
        """
        query = select(User).where(User.username == username)
        if not include_deleted:
            query = query.where(User.deleted_at.is_(None))
            
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        """Crea un nuevo usuario en la base de datos.
        
        Args:
            user_data: Datos validados para la creación del usuario
            
        Returns:
            User: Instancia del nuevo usuario creado
            
        Raises:
            DuplicateEntryException: Si el email o username ya existen
        """
        # Verifica unicidad de email y username
        if await self.get_by_email(user_data.email):
            raise DuplicateEntryException("El email ya está registrado")
            
        if user_data.username and await self.get_by_username(user_data.username):
            raise DuplicateEntryException("El nombre de usuario ya está en uso")

        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            role_id=user_data.role_id
        )
        
        try:
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            await self.db.rollback()
            raise DuplicateEntryException("Error de integridad: posible duplicado de email o username") from e

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Actualiza un usuario existente.
        
        Solo actualiza los campos que no son None en user_data.
        Verifica unicidad de email y username si son proporcionados.
        
        Args:
            user_id: ID del usuario a actualizar
            user_data: Datos validados para la actualización
            
        Returns:
            User: Instancia del usuario actualizado, None si no se encuentra
            
        Raises:
            DuplicateEntryException: Si el nuevo email o username ya existen
        """
        # Obtener datos no nulos para actualizar
        update_data = user_data.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_by_id(user_id)
            
        # Verificar unicidad si se actualiza email o username
        if 'email' in update_data:
            if await self.get_by_email(update_data['email']):
                raise DuplicateEntryException("El nuevo email ya está registrado")
                
        if 'username' in update_data and update_data['username'] is not None:
            if await self.get_by_username(update_data['username']):
                raise DuplicateEntryException("El nuevo nombre de usuario ya está en uso")
        
        # Actualizar contraseña si se proporciona
        if 'password' in update_data:
            update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
        
        try:
            result = await self.db.execute(
                update(User)
                .where(and_(User.id == user_id, User.deleted_at.is_(None)))
                .values(**update_data)
                .returning(User)
            )
            await self.db.commit()
            return result.scalar_one_or_none()
        except IntegrityError as e:
            await self.db.rollback()
            raise DuplicateEntryException("Error de integridad al actualizar usuario") from e

    async def delete(self, user_id: int) -> bool:
        """Realiza un soft delete del usuario (marca como eliminado con timestamp).
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no se encontró el usuario
        """
        result = await self.db.execute(
            update(User)
            .where(and_(User.id == user_id, User.deleted_at.is_(None)))
            .values(deleted_at=datetime.utcnow())
        )
        await self.db.commit()
        return result.rowcount > 0

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Autentica un usuario verificando email y contraseña.
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
            
        Returns:
            User: Instancia del usuario si las credenciales son válidas, None en caso contrario
            
        Raises:
            InvalidCredentialsException: Si las credenciales son inválidas
        """
        user = await self.get_by_email(email)
        if not user:
            raise InvalidCredentialsException("Credenciales inválidas")
            
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException("Credenciales inválidas")
            
        return user