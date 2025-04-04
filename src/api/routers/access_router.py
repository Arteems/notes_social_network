# Роутеры для управления правами доступа к заметкам
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.api.routers.users_router import get_user_service
from src.exceptions.user_exceptions import UserNotFoundError, InvalidUserRoleError
from src.services.users import UserService

access_router = APIRouter(prefix="/users/{user_id}/notes/{note_id}/access", tags=["Note Access"])

@access_router.post("/viewers/{viewer_id}")
async def add_note_viewer(
    user_id: str,
    note_id: str,
    viewer_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> bool:
    try:
        return await user_service.add_viewer(user_id, viewer_id, note_id)
    except (UserNotFoundError, InvalidUserRoleError) as e:
        raise HTTPException(status_code=403, detail=str(e))

@access_router.post("/editors/{editor_id}")
async def add_note_editor(
    user_id: str,
    note_id: str,
    editor_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> bool:
    try:
        return await user_service.add_editor(user_id, editor_id, note_id)
    except (UserNotFoundError, InvalidUserRoleError) as e:
        raise HTTPException(status_code=403, detail=str(e))

@access_router.delete("/viewers/{viewer_id}")
async def delete_note_viewer(
    user_id: str,
    note_id: str,
    viewer_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> bool:
    try:
        return await user_service.delete_viewer(user_id, viewer_id, note_id)
    except (UserNotFoundError, InvalidUserRoleError) as e:
        raise HTTPException(status_code=403, detail=str(e))

@access_router.delete("/editors/{editor_id}")
async def delete_note_editor(
    user_id: str,
    note_id: str,
    editor_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> bool:
    try:
        return await user_service.delete_editor(user_id, editor_id, note_id)
    except (UserNotFoundError, InvalidUserRoleError) as e:
        raise HTTPException(status_code=403, detail=str(e))