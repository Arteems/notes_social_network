from src.exceptions.note_exceptions import NoteNotFoundError
from src.exceptions.user_exceptions import InvalidUserRoleError, UserNotFoundError
from src.repositories.repository import Repository
from src.schemas.note import CreateNote, Note, UpdateNote
from src.services.notes import NoteService


class User:
    """Логика взаимодействия пользователя с записками"""

    def __init__(self, user_id: str, service: NoteService):
        self.user_id = user_id
        self.service = service

    def _check_user(self, user_id: str, role: str):
        if not user_id:
            raise UserNotFoundError(user_id=user_id)
        elif role != "Editor":
            raise InvalidUserRoleError(user_id=user_id)

    async def add_note(self, data: CreateNote) -> str:
        self._check_user(self.user_id, "Editor")
        result = await self.service.create(data)
        return result

    async def delete_note(self, role: str, note_id: str) -> bool:
        self._check_user(self.user_id, role)
        return await self.service.delete(note_id)

    async def update(self, role: str, note_id: str, update_data: UpdateNote) -> Note:
        self._check_user(self.user_id, role)
        result = await self.service.update(note_id, update_data)
        return result

    async def get(self, note_id: str) -> Note:
        self._check_user(
            self.user_id, "Viewer"
        )  # Предположим, что Viewer тоже может получать заметки
        result = await self.service.get(note_id)
        return result

    async def add_viewer(self, role: str, viewer_id: str, note_id: str) -> bool:
        self._check_user(self.user_id, role)
        return await self.service.add_viewer(viewer_id, note_id)

    async def add_editor(self, role: str, editor_id: str, note_id: str) -> bool:
        self._check_user(self.user_id, role)
        return await self.service.add_editor(editor_id, note_id)

    async def delete_viewer(self, role: str, viewer_id: str, note_id: str) -> bool:
        self._check_user(self.user_id, role)
        return await self.service.delete_viewer(viewer_id, note_id)

    async def delete_editor(self, role: str, editor_id: str, note_id: str) -> bool:
        self._check_user(self.user_id, role)
        return await self.service.delete_editor(editor_id, note_id)
