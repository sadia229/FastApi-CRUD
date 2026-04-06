from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database import AsyncSessionLocal
from infrastructure.repositories.user_repository import SQLUserRepository


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SQLUserRepository:
    return SQLUserRepository(session)
