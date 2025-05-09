from typing import Dict, Any, List
from core.entities.prediction import Prediction
from core.entities.model import MLModel
from core.repositories.prediction_repository import PredictionRepository
from core.repositories.model_repository import ModelRepository
from core.use_cases.billing_use_cases import BillingUseCases

class PredictionUseCases:
    def __init__(
        self, 
        prediction_repository: PredictionRepository,
        model_repository: ModelRepository,
        billing_use_cases: BillingUseCases,
        model_service  # Сервис для загрузки и выполнения ML-моделей
    ):
        self.prediction_repository = prediction_repository
        self.model_repository = model_repository
        self.billing_use_cases = billing_use_cases
        self.model_service = model_service
    
    async def create_prediction(self, user_id: int, model_id: int, input_data: Dict[str, Any]) -> Prediction:
        # Получаем модель
        model = await self.model_repository.get_by_id(model_id)
        if not model:
            raise ValueError(f"Модель с ID {model_id} не найдена")
        
        # Проверяем баланс пользователя
        user_balance = await self.billing_use_cases.get_user_balance(user_id)
        if user_balance < model.price:
            raise ValueError(f"Недостаточно средств на балансе. Требуется: {model.price}, Доступно: {user_balance}")
        
        # Выполняем предсказание
        prediction_result, probability = await self.model_service.predict(model.name, input_data)
        
        # Создаем запись о предсказании
        prediction = Prediction(
            user_id=user_id,
            model_id=model_id,
            input_data=input_data,
            result=prediction_result,
            probability=probability
        )
        
        # Сохраняем предсказание
        prediction = await self.prediction_repository.create(prediction)
        
        # Списываем средства с баланса
        await self.billing_use_cases.withdraw(
            user_id=user_id,
            amount=model.price,
            description=f"Оплата предсказания #{prediction.id} (модель: {model.name})",
            reference_id=prediction.id
        )
        
        return prediction
    
    async def get_prediction(self, prediction_id: int) -> Prediction:
        prediction = await self.prediction_repository.get_by_id(prediction_id)
        if not prediction:
            raise ValueError(f"Предсказание с ID {prediction_id} не найдено")
        
        return prediction
    
    async def get_user_predictions(self, user_id: int) -> List[Prediction]:
        return await self.prediction_repository.get_by_user_id(user_id)