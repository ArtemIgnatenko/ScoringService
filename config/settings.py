import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Общие настройки
    PROJECT_NAME: str = "ML Billing Service"
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # Настройки базы данных
    DATABASE_PATH: str = "ml_billing.db"
    DATABASE_ECHO: bool = False
    
    # Настройки JWT-токена
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Замените на свой секретный ключ
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Настройки ML-моделей
    MODEL_DIR: str = "models"
    
    # Настройки для моделей
    LOGISTIC_REGRESSION_PRICE: float = 25.0
    RANDOM_FOREST_PRICE: float = 50.0
    LGBM_PRICE: float = 100.0
    
    class Config:
        env_file = ".env"

settings = Settings()