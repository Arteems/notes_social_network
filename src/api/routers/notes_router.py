from typing import Optional, Annotated

from fastapi import FastAPI, HTTPException, APIRouter, Depends

from src.api.routers.users_router import get_user_service
from src.exceptions.user_exceptions import UserNotFoundError, InvalidUserRoleError
from src.repositories import notes_repository, users_repository
from src.schemas.note import CreateNote, Note, UpdateNote

from src.services.notes import NoteService
from src.services.users import UserService

# Роутер для работы с заметками
notes_router = APIRouter(prefix="/users/{user_id}/notes", tags=["Notes"])


@notes_router.post("/")
async def create_note(
    user_id: str,
    data: CreateNote,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> str:
    try:
        return await user_service.add_note(user_id, data)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@notes_router.get("/{note_id}", response_model=Note)
async def get_note(
    user_id: str,
    note_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> Note:
    try:
        return await user_service.get_note(user_id, note_id)
    except (UserNotFoundError, InvalidUserRoleError) as e:
        raise HTTPException(status_code=403, detail=str(e))

@notes_router.patch("/{note_id}", response_model=Note)
async def update_note(
    user_id: str,
    note_id: str,
    update_data: UpdateNote,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> Note:
    try:
        return await user_service.update_note(user_id, note_id, update_data)
    except (UserNotFoundError, InvalidUserRoleError) as e:
        raise HTTPException(status_code=403, detail=str(e))

@notes_router.delete("/{note_id}")
async def delete_note(
    user_id: str,
    note_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> bool:
    try:
        return await user_service.delete_note(user_id, note_id)
    except (UserNotFoundError, InvalidUserRoleError) as e:
        raise HTTPException(status_code=403, detail=str(e))
