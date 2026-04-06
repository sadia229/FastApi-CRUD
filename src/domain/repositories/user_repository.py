from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.user import UserCreate, UserRead, UserUpdate


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user_create: UserCreate) -> UserRead:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[UserRead]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserRead]:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        institution: Optional[str] = None,
    ) -> List[UserRead]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        raise NotImplementedError
