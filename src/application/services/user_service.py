from typing import List, Optional

from fastapi import HTTPException, status

from domain.entities.user import UserCreate, UserRead, UserUpdate
from domain.repositories.user_repository import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_create: UserCreate) -> UserRead:
        existing_user = await self.user_repository.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists",
            )
        return await self.user_repository.create(user_create)

    async def get_user(self, user_id: int) -> UserRead:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def list_users(
        self,
        skip: int = 0,
        limit: int = 100,
        institution: Optional[str] = None,
    ) -> List[UserRead]:
        return await self.user_repository.list(skip=skip, limit=limit, institution=institution)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserRead:
        if user_update.email is not None:
            existing_user = await self.user_repository.get_by_email(user_update.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A user with this email already exists",
                )

        updated_user = await self.user_repository.update(user_id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return updated_user

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.user_repository.delete(user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
