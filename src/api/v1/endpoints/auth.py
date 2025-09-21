# app/api/v1/endpoints/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.security import create_access_token, verify_password
from src.core.deps import get_current_user
from src.db.session import get_db
from src.db.repositories.user_repository import UserRepository
from src.schemas.auth import Token
from src.schemas.user import UserLogin, UserCreate, UserResponse, SingleUserResponse, UserChangePassword, UserLoginResponse
from src.services.user_service import UserService
from src.core.exceptions import InvalidCredentialsException, DuplicateEntryException, NotFoundException
from src.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=UserLoginResponse)
async def login_for_access_token(form_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return access token"""
    user_repo = UserRepository(db)
    try:
        user = await user_repo.authenticate(form_data.email, form_data.password)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return UserLoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            user=UserResponse.from_orm(user)
        )
    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=SingleUserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    user_service = UserService(db)
    try:
        user = await user_service.create_user(user_data)
        return SingleUserResponse(message="User registered successfully", data=user)
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/change-password", response_model=SingleUserResponse)
async def change_password(
    password_data: UserChangePassword,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change user password"""
    user_service = UserService(db)
    try:
        success = await user_service.change_user_password(
            user_id=current_user.id,
            current_password=password_data.current_password,
            new_password=password_data.new_password
        )
        if success:
            return SingleUserResponse(message="Password changed successfully", data=None)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to change password")
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))