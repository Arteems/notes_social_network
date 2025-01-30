from src.exceptions.note_exceptions import NoteNotFoundError
from src.exceptions.user_exceptions import UserNotFoundError
from src.repositories.repository import Repository
from src.schemas.note import CreateNote, Note, UpdateNote
from src.services.notes import NoteService


class User:
    ''' Логика взаимодействия пользователя с записками '''
    def __init__(self, user_id, service: NoteService):
        self.user_id = user_id
        self.service = service

    async def add_note(self, user_id: str, data: CreateNote) -> str:
        if not user_id:
            raise UserNotFoundError(user_id=user_id)
        result = await self.service.create(data)
        return result

    async def delete_note(self, user_id: str, note_id: str) -> bool:
        if user_id:
            note = await self.service.get(note_id)
            if await self.service.delete(note.id):
                return True
            return False
        raise UserNotFoundError(user_id=user_id)

    async def update(self, user_id: str, note_id: str, update_data: UpdateNote) -> Note:
        if not user_id:
            raise UserNotFoundError(user_id=user_id)
        result = await self.service.update(note_id, update_data)
        return Note(**result)

    async def get(self, user_id: str, note_id: str) -> Note:
        if not user_id:
            raise UserNotFoundError(user_id=user_id)
        result = await self.service.get(note_id)
        return result

    async def add_viewer(self, user_id: str, viewer_id: str, note_id: str) -> bool:
        if not user_id:
            raise UserNotFoundError(user_id=user_id)
        result = await self.service.add_viewer(viewer_id, note_id)
        if result:
            return True
        return False

    async def add_editor(self, user_id: str, editor_id: str, note_id) -> bool:
        if not user_id:
            raise UserNotFoundError(user_id=user_id)
        result = await self.service.add_editor(editor_id, note_id)
        if result:
            return True
        return False

    async def delete_viewer(self, user_id: str, viewer_id: str, note_id: str) -> bool:
        if not user_id:
            raise UserNotFoundError(user_id=user_id)
        return await self.service.delete_viewer(viewer_id, note_id)

    async def delete_editor(self, user_id: str, editor_id: str, note_id: str) -> bool:
        if not user_id:
            raise UserNotFoundError(user_id=user_id)
        return await self.service.delete_editor(editor_id, note_id)




