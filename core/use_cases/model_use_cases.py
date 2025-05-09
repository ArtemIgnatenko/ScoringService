from typing import List, Optional
from core.entities.model import MLModel
from core.repositories.model_repository import ModelRepository

class ModelUseCases:
    def __init__(self, model_repository: ModelRepository):
        self.model_repository = model_repository
    
    async def create_model(self, name: str, description: str, price: float, file_path: str) -> MLModel:
        # Проверяем, что модель с таким именем не существует
        existing_model = await self.model_repository.get_by_name(name)
        if existing_model:
            raise ValueError("Модель с таким именем уже существует")
        
        # Создаем новую модель
        model = MLModel(
            name=name,
            description=description,
            price=price,
            file_path=file_path,
            is_active=True
        )
        
        return await self.model_repository.create(model)
    
    async def get_model(self, model_id: int) -> Optional[MLModel]:
        return await self.model_repository.get_by_id(model_id)
    
    async def get_model_by_name(self, name: str) -> Optional[MLModel]:
        return await self.model_repository.get_by_name(name)
    
    async def list_models(self) -> List[MLModel]:
        return await self.model_repository.list()
    
    async def update_model(self, model: MLModel) -> MLModel:
        existing_model = await self.model_repository.get_by_id(model.id)
        if not existing_model:
            raise ValueError(f"Модель с ID {model.id} не найдена")
        
        return await self.model_repository.update(model)
    
    async def delete_model(self, model_id: int) -> bool:
        existing_model = await self.model_repository.get_by_id(model_id)
        if not existing_model:
            raise ValueError(f"Модель с ID {model_id} не найдена")
        
        return await self.model_repository.delete(model_id)