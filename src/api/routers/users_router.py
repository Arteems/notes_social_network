from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr

from schemas.users import CreateUser, UpdateUser, User
from services import user_service

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/")
async def create_user(user: CreateUser) -> str:
    return await user_service.create(user)


@users_router.get("/{user_id}", response_model=User)
async def get_user(user: Annotated[User, Depends(user_service.get)]) -> User:
    return user


@users_router.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    new_data: UpdateUser,
) -> User:
    return await user_service.update(user_id, new_data)


@users_router.delete("/{user_id}")
async def delete_user(user_id: str) -> bool:
    return await user_service.delete(user_id)


# Роутер для работы с почтой пользователя
@users_router.patch("/{user_id}/mail", response_model=User)
async def update_user_mail(
    user_id: str,
    new_mail: EmailStr,
) -> User:
    return await user_service.update_mail(user_id, new_mail)


# Роутер для работы с паролем пользователя
@users_router.patch("/{user_id}/password", response_model=User)
async def update_user_password(
    user_id: str,
    new_password: str,
) -> User:
    return await user_service.update_password(user_id, new_password)
