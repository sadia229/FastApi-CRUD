from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import UserCreate, UserRead, UserUpdate
from domain.repositories.user_repository import IUserRepository
from infrastructure.database.models import UserModel


class SQLUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_create: UserCreate) -> UserRead:
        db_user = UserModel(**user_create.model_dump())
        self.session.add(db_user)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(db_user)
        return UserRead.model_validate(db_user)

    async def get_by_id(self, user_id: int) -> Optional[UserRead]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        db_user = result.scalar_one_or_none()
        return UserRead.model_validate(db_user) if db_user else None

    async def get_by_email(self, email: str) -> Optional[UserRead]:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        db_user = result.scalar_one_or_none()
        return UserRead.model_validate(db_user) if db_user else None

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        institution: Optional[str] = None,
    ) -> List[UserRead]:
        query = select(UserModel).order_by(UserModel.id.desc()).offset(skip).limit(limit)
        if institution:
            query = query.where(UserModel.institution == institution)
        result = await self.session.execute(query)
        return [UserRead.model_validate(user) for user in result.scalars().all()]

    async def update(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None

        for field_name, field_value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, field_name, field_value)

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(db_user)
        return UserRead.model_validate(db_user)

    async def delete(self, user_id: int) -> bool:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        db_user = result.scalar_one_or_none()
        if not db_user:
            return False

        await self.session.delete(db_user)
        await self.session.commit()
        return True
