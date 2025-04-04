# Роутеры для управления правами доступа к заметкам
from fastapi import APIRouter
from services import user_service


access_router = APIRouter(
    prefix="/users/{user_id}/notes/{note_id}/access", tags=["Note Access"]
)


@access_router.post("/viewers/{viewer_id}")
async def add_note_viewer(
    user_id: str,
    note_id: str,
    viewer_id: str,
) -> bool:
    return await user_service.add_viewer(user_id, viewer_id, note_id)


@access_router.post("/editors/{editor_id}")
async def add_note_editor(
    user_id: str,
    note_id: str,
    editor_id: str,
) -> bool:
    return await user_service.add_editor(user_id, editor_id, note_id)


@access_router.delete("/viewers/{viewer_id}")
async def delete_note_viewer(
    user_id: str,
    note_id: str,
    viewer_id: str,
) -> bool:
    return await user_service.delete_viewer(user_id, viewer_id, note_id)


@access_router.delete("/editors/{editor_id}")
async def delete_note_editor(
    user_id: str,
    note_id: str,
    editor_id: str,
) -> bool:
    return await user_service.delete_editor(user_id, editor_id, note_id)
