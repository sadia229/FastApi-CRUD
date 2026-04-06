from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError

from application.services.user_service import UserService
from domain.entities.user import UserCreate, UserRead, UserUpdate
from infrastructure.repositories.user_repository import SQLUserRepository
from presentation.dependencies import get_user_repository

router = APIRouter(prefix="/users", tags=["users"])
UserRepositoryDependency = Annotated[SQLUserRepository, Depends(get_user_repository)]


def _service(user_repository: SQLUserRepository) -> UserService:
    return UserService(user_repository)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, user_repository: UserRepositoryDependency) -> UserRead:
    try:
        return await _service(user_repository).create_user(user_create)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        ) from exc


@router.get("/", response_model=list[UserRead])
async def list_users(
    user_repository: UserRepositoryDependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    institution: Optional[str] = Query(default=None),
) -> list[UserRead]:
    return await _service(user_repository).list_users(
        skip=skip,
        limit=limit,
        institution=institution,
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, user_repository: UserRepositoryDependency) -> UserRead:
    return await _service(user_repository).get_user(user_id)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_repository: UserRepositoryDependency,
) -> UserRead:
    try:
        return await _service(user_repository).update_user(user_id, user_update)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        ) from exc


@router.patch("/{user_id}", response_model=UserRead)
async def patch_user(
    user_id: int,
    user_update: UserUpdate,
    user_repository: UserRepositoryDependency,
) -> UserRead:
    try:
        return await _service(user_repository).update_user(user_id, user_update)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        ) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_repository: UserRepositoryDependency) -> Response:
    await _service(user_repository).delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
