from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from core.entities.user import User
from core.repositories.user_repository import UserRepository
from infrastructure.db.models import UserModel

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        db_user = UserModel(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            balance=user.balance,
            is_active=user.is_active
        )
        
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            balance=db_user.balance,
            is_active=db_user.is_active
        )
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        db_user = result.scalars().first()
        
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            balance=db_user.balance,
            is_active=db_user.is_active
        )
    
    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(select(UserModel).where(UserModel.username == username))
        db_user = result.scalars().first()
        
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            balance=db_user.balance,
            is_active=db_user.is_active
        )
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        db_user = result.scalars().first()
        
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            balance=db_user.balance,
            is_active=db_user.is_active
        )
    
    async def update(self, user: User) -> User:
        await self.session.execute(
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                balance=user.balance,
                is_active=user.is_active
            )
        )
        await self.session.commit()
        
        return await self.get_by_id(user.id)
    
    async def delete(self, user_id: int) -> bool:
        await self.session.execute(delete(UserModel).where(UserModel.id == user_id))
        await self.session.commit()
        return True
    
    async def list(self) -> List[User]:
        result = await self.session.execute(select(UserModel))
        db_users = result.scalars().all()
        
        return [
            User(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email,
                password_hash=db_user.password_hash,
                balance=db_user.balance,
                is_active=db_user.is_active
            )
            for db_user in db_users
        ]
    

# Аналогичным образом реализуем остальные репозитории
# infrastructure/db/repositories/model_repository_impl.py, prediction_repository_impl.py, transaction_repository_impl.py