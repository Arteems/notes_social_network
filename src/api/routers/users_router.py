from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from pydantic import EmailStr

from src.repositories.repository import Repository
from src.services.users import UserService
from src.services.notes import NoteService
from src.repositories import users_repository, notes_repository
from src.schemas.users import CreateUser, User, UpdateUser
from src.schemas.note import CreateNote, UpdateNote, Note
from src.exceptions.user_exceptions import UserNotFoundError, InvalidUserRoleError, UserUpdateError


users_router = APIRouter(prefix="/users", tags=["Users"])


def get_notes_repository():
    return notes_repository

# Функция для получения сервиса заметок
def get_note_service(
    notes_repo: Annotated[Repository, Depends(get_notes_repository)]
) -> NoteService:
    return NoteService(notes_repository)

def get_user_service(
    note_service: Annotated[NoteService, Depends(get_note_service)]
):
    return UserService(users_repository, note_service)



@users_router.post("/")
async def create_user(
    user: CreateUser,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> str:
    try:
        return await user_service.create(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@users_router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    try:
        return await user_service.get(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@users_router.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    new_data: UpdateUser,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    try:
        return await user_service.update(user_id, new_data)
    except (UserNotFoundError, UserUpdateError) as e:
        raise HTTPException(status_code=404, detail=str(e))

@users_router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> bool:
    try:
        return await user_service.delete(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Роутер для работы с почтой пользователя
@users_router.patch("/{user_id}/mail", response_model=User)
async def update_user_mail(
    user_id: str,
    new_mail: EmailStr,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    try:
        return await user_service.update_mail(user_id, new_mail)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Роутер для работы с паролем пользователя
@users_router.patch("/{user_id}/password", response_model=User)
async def update_user_password(
    user_id: str,
    new_password: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    try:
        return await user_service.update_password(user_id, new_password)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))





