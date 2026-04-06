import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


def _default_database_url() -> str:
    return "sqlite+aiosqlite:///./app.db"


DATABASE_URL = os.getenv("DATABASE_URL", _default_database_url())
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "false").lower() == "true"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=DATABASE_ECHO, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
