from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal

@dataclass
class Transaction:
    id: Optional[int] = None
    user_id: int = 0
    amount: float = 0.0  # Положительное - пополнение, отрицательное - списание
    transaction_type: Literal["DEPOSIT", "WITHDRAW", "PREDICTION"] = "DEPOSIT"
    description: str = ""
    reference_id: Optional[int] = None  # ID предсказания или другой ссылки
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()