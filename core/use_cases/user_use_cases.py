from typing import Optional
from passlib.context import CryptContext
from core.entities.user import User
from core.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    async def register_user(self, username: str, email: str, password: str) -> User:
        # Проверяем, что пользователь с таким email не существует
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует")
        
        # Проверяем, что пользователь с таким username не существует
        existing_user = await self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError("Пользователь с таким username уже существует")
        
        # Создаем нового пользователя
        password_hash = self.hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            balance=100.0  # Начальный баланс
        )
        
        return await self.user_repository.create(user)
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        return user
    
    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)
    
    async def list_users(self):
        return await self.user_repository.list()
