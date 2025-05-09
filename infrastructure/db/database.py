from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

# SQLAlchemy URL для асинхронной SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{settings.DATABASE_PATH}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
    connect_args={"check_same_thread": False}  # Для SQLite
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """Зависимость для FastAPI, которая предоставляет сессию БД"""
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
