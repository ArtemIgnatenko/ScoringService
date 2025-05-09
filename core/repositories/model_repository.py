from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.model import MLModel

class ModelRepository(ABC):
    @abstractmethod
    async def create(self, model: MLModel) -> MLModel:
        pass
    
    @abstractmethod
    async def get_by_id(self, model_id: int) -> Optional[MLModel]:
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[MLModel]:
        pass
    
    @abstractmethod
    async def update(self, model: MLModel) -> MLModel:
        pass
    
    @abstractmethod
    async def delete(self, model_id: int) -> bool:
        pass
    
    @abstractmethod
    async def list(self) -> List[MLModel]:
        pass