from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.entities.user import User
from core.use_cases.user_use_cases import UserUseCases
from infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.database import get_db
from infrastructure.web.schemas import UserResponse
from infrastructure.web.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user