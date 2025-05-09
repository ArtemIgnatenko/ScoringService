# main.py
import asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from infrastructure.db.database import Base, engine
from infrastructure.web.api import auth, users, models, predictions, billing
from infrastructure.ml.save_models import save_models


# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене стоит заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры API
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(users.router, prefix=settings.API_PREFIX)
app.include_router(models.router, prefix=settings.API_PREFIX)
app.include_router(predictions.router, prefix=settings.API_PREFIX)
app.include_router(billing.router, prefix=settings.API_PREFIX)

# Создаем таблицы и инициализируем данные
async def setup_db():
    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Проверяем наличие моделей
    if not os.path.exists(settings.MODEL_DIR):
        os.makedirs(settings.MODEL_DIR)
        
        # Инициализируем модели (в реальном проекте может потребоваться отдельный скрипт)
        try:
            save_models()
        except Exception as e:
            print(f"Не удалось сохранить модели: {e}")

@app.on_event("startup")
async def startup():
    await setup_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)