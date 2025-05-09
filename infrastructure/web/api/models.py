from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.entities.user import User
from core.use_cases.model_use_cases import ModelUseCases
from infrastructure.db.repositories.model_repository_impl import ModelRepositoryImpl
from infrastructure.db.database import get_db
from infrastructure.web.schemas import MLModelResponse
from infrastructure.web.dependencies import get_current_user

router = APIRouter(prefix="/models", tags=["models"])

@router.get("/", response_model=List[MLModelResponse])
async def list_models(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    model_repository = ModelRepositoryImpl(db)
    model_use_cases = ModelUseCases(model_repository)
    
    models = await model_use_cases.list_models()
    return models

@router.get("/{model_id}", response_model=MLModelResponse)
async def get_model(
    model_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    model_repository = ModelRepositoryImpl(db)
    model_use_cases = ModelUseCases(model_repository)
    
    model = await model_use_cases.get_model(model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Модель с ID {model_id} не найдена"
        )
    
    return model
