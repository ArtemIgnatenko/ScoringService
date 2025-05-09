from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class Prediction:
    id: Optional[int] = None
    user_id: int = 0
    model_id: int = 0
    input_data: Dict[str, Any] = None
    result: Any = None
    probability: float = 0.0  # Вероятность результата
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()