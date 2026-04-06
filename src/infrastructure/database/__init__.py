import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


def _default_database_url() -> str:
    return "sqlite+aiosqlite:///./app.db"


def _normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql+asyncpg://"):
        return database_url
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+asyncpg://", 1)
    return database_url


DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL", _default_database_url()))
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "false").lower() == "true"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=DATABASE_ECHO, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
