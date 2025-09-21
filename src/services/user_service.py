# app/services/user_service.py
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.db.repositories.user_repository import UserRepository
from src.schemas.user import UserCreate, UserUpdate
from src.models.user import User
from src.core.exceptions import NotFoundException


class UserService:
    """
    Servicio para gestionar la lógica de negocio de usuarios.

    Proporciona una capa de abstracción sobre el repositorio de usuarios,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión de base de datos asíncrona.
        """
        self.user_repo = UserRepository(db)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario a buscar.

        Returns:
            El usuario si se encuentra, de lo contrario None.
        """
        return await self.user_repo.get_by_id(user_id)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Obtiene una lista de todos los usuarios con paginación.

        Args:
            skip: Número de registros a saltar.
            limit: Número máximo de registros a devolver.

        Returns:
            Una lista de usuarios.
        """
        return await self.user_repo.get_all(skip=skip, limit=limit)

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Crea un nuevo usuario.

        Args:
            user_data: Datos para la creación del usuario.

        Returns:
            El usuario recién creado.
        """
        return await self.user_repo.create(user_data)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Actualiza un usuario existente.

        Args:
            user_id: ID del usuario a actualizar.
            user_data: Datos para la actualización.

        Returns:
            El usuario actualizado si se encuentra, de lo contrario None.
        
        Raises:
            NotFoundException: Si el usuario no se encuentra.
        """
        user = await self.user_repo.update(user_id, user_data)
        if not user:
            raise NotFoundException("Usuario no encontrado")
        return user

    async def delete_user(self, user_id: int) -> bool:
        """
        Elimina (soft delete) un usuario.

        Args:
            user_id: ID del usuario a eliminar.

        Returns:
            True si el usuario fue eliminado, False en caso contrario.
        
        Raises:
            NotFoundException: Si el usuario no se encuentra.
        """
        success = await self.user_repo.delete(user_id)
        if not success:
            raise NotFoundException("Usuario no encontrado")
        return success

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su dirección de correo electrónico.

        Args:
            email: Correo electrónico del usuario.

        Returns:
            El usuario si se encuentra, de lo contrario None.
        """
        return await self.user_repo.get_by_email(email)

    async def change_user_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Cambia la contraseña de un usuario después de verificar la contraseña actual.

        Args:
            user_id: ID del usuario.
            current_password: Contraseña actual del usuario.
            new_password: Nueva contraseña del usuario.

        Returns:
            True si la contraseña se cambió correctamente.

        Raises:
            NotFoundException: Si el usuario no se encuentra.
            InvalidCredentialsException: Si la contraseña actual es incorrecta.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuario no encontrado")
            
        if not verify_password(current_password, user.hashed_password):
            raise InvalidCredentialsException("La contraseña actual es incorrecta")
            
        # Update the password
        user_update = UserUpdate(password=new_password)
        updated_user = await self.user_repo.update(user_id, user_update)
        return updated_user is not None
