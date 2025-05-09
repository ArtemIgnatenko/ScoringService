from dataclasses import dataclass
from typing import Optional

@dataclass
class MLModel:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    price: float = 0.0  # Стоимость использования модели
    file_path: str = ""
    is_active: bool = True