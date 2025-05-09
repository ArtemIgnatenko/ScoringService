from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from core.use_cases.user_use_cases import UserUseCases
from infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.database import get_db
from infrastructure.web.schemas import Token, UserCreate, UserResponse
from infrastructure.web.dependencies import create_access_token
from config.settings import settings

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    user_repository = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repository)
    
    try:
        user = await user_use_cases.register_user(
            username=user_create.username,
            email=user_create.email,
            password=user_create.password
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user_repository = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repository)
    
    user = await user_use_cases.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
