# app/api/v1/endpoints/user.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.services.user_service import UserService
from src.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse, SingleUserResponse
from src.core.exceptions import NotFoundException, DuplicateEntryException

router = APIRouter()


@router.post("/", response_model=SingleUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, user_service: UserService = Depends()):
    """
    Crea un nuevo usuario.
    """
    try:
        user = await user_service.create_user(user_data)
        return SingleUserResponse(message="Usuario creado con éxito", data=user)
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{user_id}", response_model=SingleUserResponse)
async def get_user(user_id: int, user_service: UserService = Depends()):
    """
    Obtiene un usuario por su ID.
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return SingleUserResponse(message="Usuario obtenido con éxito", data=user)


@router.get("/", response_model=UserListResponse)
async def get_all_users(skip: int = 0, limit: int = 100, user_service: UserService = Depends()):
    """
    Obtiene una lista de todos los usuarios.
    """
    users = await user_service.get_all_users(skip=skip, limit=limit)
    return UserListResponse(message="Usuarios obtenidos con éxito", data=users)


@router.put("/{user_id}", response_model=SingleUserResponse)
async def update_user(user_id: int, user_data: UserUpdate, user_service: UserService = Depends()):
    """
    Actualiza un usuario existente.
    """
    try:
        user = await user_service.update_user(user_id, user_data)
        return SingleUserResponse(message="Usuario actualizado con éxito", data=user)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_service: UserService = Depends()):
    """
    Elimina un usuario.
    """
    try:
        await user_service.delete_user(user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
