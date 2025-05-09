from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.entities.transaction import Transaction
from core.repositories.transaction_repository import TransactionRepository
from infrastructure.db.models import TransactionModel

class TransactionRepositoryImpl(TransactionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, transaction: Transaction) -> Transaction:
        db_transaction = TransactionModel(
            user_id=transaction.user_id,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type,
            description=transaction.description,
            reference_id=transaction.reference_id
        )
        
        self.session.add(db_transaction)
        await self.session.commit()
        await self.session.refresh(db_transaction)
        
        return Transaction(
            id=db_transaction.id,
            user_id=db_transaction.user_id,
            amount=db_transaction.amount,
            transaction_type=db_transaction.transaction_type,
            description=db_transaction.description,
            reference_id=db_transaction.reference_id,
            created_at=db_transaction.created_at
        )
    
    async def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        result = await self.session.execute(select(TransactionModel).where(TransactionModel.id == transaction_id))
        db_transaction = result.scalars().first()
        
        if not db_transaction:
            return None
        
        return Transaction(
            id=db_transaction.id,
            user_id=db_transaction.user_id,
            amount=db_transaction.amount,
            transaction_type=db_transaction.transaction_type,
            description=db_transaction.description,
            reference_id=db_transaction.reference_id,
            created_at=db_transaction.created_at
        )
    
    async def get_by_user_id(self, user_id: int) -> List[Transaction]:
        result = await self.session.execute(select(TransactionModel).where(TransactionModel.user_id == user_id))
        db_transactions = result.scalars().all()
        
        return [
            Transaction(
                id=db_transaction.id,
                user_id=db_transaction.user_id,
                amount=db_transaction.amount,
                transaction_type=db_transaction.transaction_type,
                description=db_transaction.description,
                reference_id=db_transaction.reference_id,
                created_at=db_transaction.created_at
            )
            for db_transaction in db_transactions
        ]
    
    async def list(self) -> List[Transaction]:
        result = await self.session.execute(select(TransactionModel))
        db_transactions = result.scalars().all()
        
        return [
            Transaction(
                id=db_transaction.id,
                user_id=db_transaction.user_id,
                amount=db_transaction.amount,
                transaction_type=db_transaction.transaction_type,
                description=db_transaction.description,
                reference_id=db_transaction.reference_id,
                created_at=db_transaction.created_at
            )
            for db_transaction in db_transactions
        ]