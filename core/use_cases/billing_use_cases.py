from typing import List
from core.entities.user import User
from core.entities.transaction import Transaction
from core.repositories.user_repository import UserRepository
from core.repositories.transaction_repository import TransactionRepository

class BillingUseCases:
    def __init__(
        self, 
        user_repository: UserRepository,
        transaction_repository: TransactionRepository
    ):
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository
    
    async def deposit(self, user_id: int, amount: float, description: str = "Пополнение баланса") -> Transaction:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        
        # Создаем транзакцию
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            transaction_type="DEPOSIT",
            description=description
        )
        
        # Обновляем баланс пользователя
        user.balance += amount
        await self.user_repository.update(user)
        
        # Сохраняем транзакцию
        return await self.transaction_repository.create(transaction)
    
    async def withdraw(self, user_id: int, amount: float, description: str, reference_id: int = None) -> Transaction:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        
        if user.balance < amount:
            raise ValueError("Недостаточно средств на балансе")
        
        # Создаем транзакцию
        transaction = Transaction(
            user_id=user_id,
            amount=-amount,  # Отрицательная сумма для списания
            transaction_type="WITHDRAW" if not reference_id else "PREDICTION",
            description=description,
            reference_id=reference_id
        )
        
        # Обновляем баланс пользователя
        user.balance -= amount
        await self.user_repository.update(user)
        
        # Сохраняем транзакцию
        return await self.transaction_repository.create(transaction)
    
    async def get_user_balance(self, user_id: int) -> float:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        
        return user.balance
    
    async def get_user_transactions(self, user_id: int) -> List[Transaction]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        
        return await self.transaction_repository.get_by_user_id(user_id)