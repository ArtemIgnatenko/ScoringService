from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.entities.user import User
from core.use_cases.prediction_use_cases import PredictionUseCases
from core.use_cases.model_use_cases import ModelUseCases
from core.use_cases.billing_use_cases import BillingUseCases
from infrastructure.db.repositories.prediction_repository_impl import PredictionRepositoryImpl
from infrastructure.db.repositories.model_repository_impl import ModelRepositoryImpl
from infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.repositories.transaction_repository_impl import TransactionRepositoryImpl
from infrastructure.db.database import get_db
from infrastructure.ml.model_service import ModelService
from infrastructure.web.schemas import PredictionCreate, PredictionResponse
from infrastructure.web.dependencies import get_current_user

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/", response_model=PredictionResponse)
async def create_prediction(
    prediction_create: PredictionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Создаем репозитории
    prediction_repository = PredictionRepositoryImpl(db)
    model_repository = ModelRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    transaction_repository = TransactionRepositoryImpl(db)
    
    # Создаем сервисы
    model_service = ModelService()
    billing_use_cases = BillingUseCases(user_repository, transaction_repository)
    
    # Создаем use case для предсказания
    prediction_use_cases = PredictionUseCases(
        prediction_repository=prediction_repository,
        model_repository=model_repository,
        billing_use_cases=billing_use_cases,
        model_service=model_service
    )
    
    try:
        # Преобразуем входные данные в словарь
        input_data_dict = prediction_create.input_data.dict()
        
        # Создаем предсказание
        prediction = await prediction_use_cases.create_prediction(
            user_id=current_user.id,
            model_id=prediction_create.model_id,
            input_data=input_data_dict
        )
        
        return prediction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[PredictionResponse])
async def list_predictions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    prediction_repository = PredictionRepositoryImpl(db)
    model_repository = ModelRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    transaction_repository = TransactionRepositoryImpl(db)
    
    model_service = ModelService()
    billing_use_cases = BillingUseCases(user_repository, transaction_repository)
    
    prediction_use_cases = PredictionUseCases(
        prediction_repository=prediction_repository,
        model_repository=model_repository,
        billing_use_cases=billing_use_cases,
        model_service=model_service
    )
    
    predictions = await prediction_use_cases.get_user_predictions(current_user.id)
    return predictions

@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    prediction_repository = PredictionRepositoryImpl(db)
    model_repository = ModelRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    transaction_repository = TransactionRepositoryImpl(db)
    
    model_service = ModelService()
    billing_use_cases = BillingUseCases(user_repository, transaction_repository)
    
    prediction_use_cases = PredictionUseCases(
        prediction_repository=prediction_repository,
        model_repository=model_repository,
        billing_use_cases=billing_use_cases,
        model_service=model_service
    )
    
    try:
        prediction = await prediction_use_cases.get_prediction(prediction_id)
        
        # Проверяем, что предсказание принадлежит текущему пользователю
        if prediction.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет доступа к этому предсказанию"
            )
        
        return prediction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )