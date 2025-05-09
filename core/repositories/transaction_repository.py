from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.transaction import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    async def create(self, transaction: Transaction) -> Transaction:
        pass
    
    @abstractmethod
    async def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[Transaction]:
        pass
    
    @abstractmethod
    async def list(self) -> List[Transaction]:
        pass