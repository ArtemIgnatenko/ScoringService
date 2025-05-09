from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.prediction import Prediction

class PredictionRepository(ABC):
    @abstractmethod
    async def create(self, prediction: Prediction) -> Prediction:
        pass
    
    @abstractmethod
    async def get_by_id(self, prediction_id: int) -> Optional[Prediction]:
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[Prediction]:
        pass
    
    @abstractmethod
    async def list(self) -> List[Prediction]:
        pass