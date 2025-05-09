from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from core.entities.model import MLModel
from core.repositories.model_repository import ModelRepository
from infrastructure.db.models import MLModelModel

class ModelRepositoryImpl(ModelRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, model: MLModel) -> MLModel:
        db_model = MLModelModel(
            name=model.name,
            description=model.description,
            price=model.price,
            file_path=model.file_path,
            is_active=model.is_active
        )
        
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        
        return MLModel(
            id=db_model.id,
            name=db_model.name,
            description=db_model.description,
            price=db_model.price,
            file_path=db_model.file_path,
            is_active=db_model.is_active
        )
    
    async def get_by_id(self, model_id: int) -> Optional[MLModel]:
        result = await self.session.execute(select(MLModelModel).where(MLModelModel.id == model_id))
        db_model = result.scalars().first()
        
        if not db_model:
            return None
        
        return MLModel(
            id=db_model.id,
            name=db_model.name,
            description=db_model.description,
            price=db_model.price,
            file_path=db_model.file_path,
            is_active=db_model.is_active
        )
    
    async def get_by_name(self, name: str) -> Optional[MLModel]:
        result = await self.session.execute(select(MLModelModel).where(MLModelModel.name == name))
        db_model = result.scalars().first()
        
        if not db_model:
            return None
        
        return MLModel(
            id=db_model.id,
            name=db_model.name,
            description=db_model.description,
            price=db_model.price,
            file_path=db_model.file_path,
            is_active=db_model.is_active
        )
    
    async def update(self, model: MLModel) -> MLModel:
        await self.session.execute(
            update(MLModelModel)
            .where(MLModelModel.id == model.id)
            .values(
                name=model.name,
                description=model.description,
                price=model.price,
                file_path=model.file_path,
                is_active=model.is_active
            )
        )
        await self.session.commit()
        
        return await self.get_by_id(model.id)
    
    async def delete(self, model_id: int) -> bool:
        await self.session.execute(delete(MLModelModel).where(MLModelModel.id == model_id))
        await self.session.commit()
        return True
    
    async def list(self) -> List[MLModel]:
        result = await self.session.execute(select(MLModelModel))
        db_models = result.scalars().all()
        
        return [
            MLModel(
                id=db_model.id,
                name=db_model.name,
                description=db_model.description,
                price=db_model.price,
                file_path=db_model.file_path,
                is_active=db_model.is_active
            )
            for db_model in db_models
        ]