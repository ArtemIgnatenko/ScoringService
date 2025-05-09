from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.entities.prediction import Prediction
from core.repositories.prediction_repository import PredictionRepository
from infrastructure.db.models import PredictionModel

class PredictionRepositoryImpl(PredictionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, prediction: Prediction) -> Prediction:
        db_prediction = PredictionModel(
            user_id=prediction.user_id,
            model_id=prediction.model_id,
            input_data=prediction.input_data,
            result=prediction.result,
            probability=prediction.probability
        )
        
        self.session.add(db_prediction)
        await self.session.commit()
        await self.session.refresh(db_prediction)
        
        return Prediction(
            id=db_prediction.id,
            user_id=db_prediction.user_id,
            model_id=db_prediction.model_id,
            input_data=db_prediction.input_data,
            result=db_prediction.result,
            probability=db_prediction.probability,
            created_at=db_prediction.created_at
        )
    
    async def get_by_id(self, prediction_id: int) -> Optional[Prediction]:
        result = await self.session.execute(select(PredictionModel).where(PredictionModel.id == prediction_id))
        db_prediction = result.scalars().first()
        
        if not db_prediction:
            return None
        
        return Prediction(
            id=db_prediction.id,
            user_id=db_prediction.user_id,
            model_id=db_prediction.model_id,
            input_data=db_prediction.input_data,
            result=db_prediction.result,
            probability=db_prediction.probability,
            created_at=db_prediction.created_at
        )
    
    async def get_by_user_id(self, user_id: int) -> List[Prediction]:
        result = await self.session.execute(select(PredictionModel).where(PredictionModel.user_id == user_id))
        db_predictions = result.scalars().all()
        
        return [
            Prediction(
                id=db_prediction.id,
                user_id=db_prediction.user_id,
                model_id=db_prediction.model_id,
                input_data=db_prediction.input_data,
                result=db_prediction.result,
                probability=db_prediction.probability,
                created_at=db_prediction.created_at
            )
            for db_prediction in db_predictions
        ]
    
    async def list(self) -> List[Prediction]:
        result = await self.session.execute(select(PredictionModel))
        db_predictions = result.scalars().all()
        
        return [
            Prediction(
                id=db_prediction.id,
                user_id=db_prediction.user_id,
                model_id=db_prediction.model_id,
                input_data=db_prediction.input_data,
                result=db_prediction.result,
                probability=db_prediction.probability,
                created_at=db_prediction.created_at
            )
            for db_prediction in db_predictions
        ]