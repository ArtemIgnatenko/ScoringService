from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime

# Схемы для пользователей
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    balance: float
    is_active: bool
    
    class Config:
        orm_mode = True

class UserAuth(BaseModel):
    username: str
    password: str

# Схемы для токенов
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

# Схемы для моделей ML
class MLModelBase(BaseModel):
    name: str
    description: str
    price: float

class MLModelCreate(MLModelBase):
    file_path: str

class MLModelResponse(MLModelBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True

# Схемы для предсказаний
class PredictionInput(BaseModel):
    person_age: int
    person_income: int
    person_home_ownership: str
    person_emp_length: float
    loan_intent: str
    loan_grade: str
    loan_amnt: int
    loan_int_rate: float
    loan_percent_income: float
    cb_person_default_on_file: str
    cb_person_cred_hist_length: int
    
    class Config:
        schema_extra = {
            "example": {
                "person_age": 30,
                "person_income": 50000,
                "person_home_ownership": "RENT",
                "person_emp_length": 5.0,
                "loan_intent": "EDUCATION",
                "loan_grade": "A",
                "loan_amnt": 10000,
                "loan_int_rate": 12.5,
                "loan_percent_income": 0.2,
                "cb_person_default_on_file": "N",
                "cb_person_cred_hist_length": 3
            }
        }

class PredictionCreate(BaseModel):
    model_id: int
    input_data: PredictionInput

class PredictionResponse(BaseModel):
    id: int
    user_id: int
    model_id: int
    input_data: Dict[str, Any]
    result: int
    probability: float
    created_at: datetime
    
    class Config:
        orm_mode = True

# Схемы для транзакций
class TransactionBase(BaseModel):
    amount: float
    description: str = Field(default="")

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    transaction_type: str
    reference_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        orm_mode = True
