from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.entities.user import User
from core.use_cases.billing_use_cases import BillingUseCases
from infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.repositories.transaction_repository_impl import TransactionRepositoryImpl
from infrastructure.db.database import get_db
from infrastructure.web.schemas import TransactionCreate, TransactionResponse
from infrastructure.web.dependencies import get_current_user

router = APIRouter(prefix="/billing", tags=["billing"])

@router.post("/deposit", response_model=TransactionResponse)
async def deposit(
    transaction_create: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_repository = UserRepositoryImpl(db)
    transaction_repository = TransactionRepositoryImpl(db)
    
    billing_use_cases = BillingUseCases(user_repository, transaction_repository)
    
    try:
        transaction = await billing_use_cases.deposit(
            user_id=current_user.id,
            amount=transaction_create.amount,
            description=transaction_create.description or "Пополнение баланса"
        )
        
        return transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/transactions", response_model=List[TransactionResponse])
async def list_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_repository = UserRepositoryImpl(db)
    transaction_repository = TransactionRepositoryImpl(db)
    
    billing_use_cases = BillingUseCases(user_repository, transaction_repository)
    
    transactions = await billing_use_cases.get_user_transactions(current_user.id)
    return transactions