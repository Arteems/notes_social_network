from fastapi import APIRouter, Depends, HTTPException

from schemas.note import CreateNote, Note, UpdateNote
from services import user_service

# Роутер для работы с заметками
notes_router = APIRouter(prefix="/notes", tags=["Notes"])


@notes_router.post("/")
async def create_note(
    user_id: str,
    data: CreateNote,
) -> str:
    return await user_service.add_note(user_id, data)


@notes_router.get("/{note_id}", response_model=Note)
async def get_note(
    user_id: str,
    note_id: str,
) -> Note:
    return await user_service.get_note(user_id, note_id)


@notes_router.patch("/{note_id}", response_model=Note)
async def update_note(
    user_id: str,
    note_id: str,
    update_data: UpdateNote,
) -> Note:
    return await user_service.update_note(user_id, note_id, update_data)


@notes_router.delete("/{note_id}")
async def delete_note(
    user_id: str,
    note_id: str,
) -> bool:
    return await user_service.delete_note(user_id, note_id)
