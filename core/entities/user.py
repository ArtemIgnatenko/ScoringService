from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    balance: float = 100.0  # Начальный баланс 100 кредитов
    is_active: bool = True