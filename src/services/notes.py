from ..repositories.notes import Repository
from ..schemas.note import Viewer, Editor, Note, UpdateNote
from ..exceptions.exceptions import NoteUpdateError, NoteCreateError, NoteDeleteError, NoteNotFoundError


class NoteService:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def get(self, note_id: str) -> dict:
        existing_note = await self.get(note_id)
        if not existing_note:
            raise NoteNotFoundError(note_id)
        return existing_note

    async def create(self, note: Note) -> str:
        try:
            result = await self.repository.create(note.model_dump())
            return result
        except Exception as e:
            raise NoteCreateError("Ошибка при создании заметки") from e

    async def update(self, note_id: str, new_data: UpdateNote) -> dict:
        await self.get(note_id)

        try:
            result = await self.repository.update(note_id, new_data.model_dump(exclude_unset=True))
            return result
        except Exception as e:
            raise NoteUpdateError("ошибка при обновлении заметки") from e

    async def delete(self, note_id: str) -> bool:
        existing_note = await self.get(note_id)
        if not existing_note:
            raise NoteNotFoundError("заметка не найдена")

        try:
            result = await self.repository.delete(note_id)
            return result
        except Exception as e:
            raise NoteDeleteError("ошибка при удалении заметки") from e

    # async def delete_viewer(self, note_id: str, viewer_id: str) -> bool:
    #     note = await self.repository.get(note_id)
    #     if not note:
    #         return False
    #
    #     note = Note(note, from )
    #     if viewer_id in note.viewers.:
    #         await self.repository.delete_view(viewer_id)
    #
    #     updated_users = [
    #         user for user in note.authorised_users
    #         if not (isinstance(user, Viewer) and user.id == viewer_id.id)
    #     ]
    #
    #     result = await self.repository.update(note_id, {"authorised_users": updated_users})
    #
    #     return result is not None and result[0] > 0
    #
    # async def delete_editor(self, note: Note, editor_id: Editor) -> bool:
    #     note_id = note.id
    #     document = await self.get(note_id)
    #     if not document:
    #         return False
    #
    #     if editor_id in note.authorised_users:
    #         await self.repository.delete_edit(editor_id)
    #
    #     updated_users = [
    #         user for user in note.authorised_users
    #         if not (isinstance(user, Editor) and user.id == editor_id.id)
    #     ]
    #
    #     result = await self.repository.update(note_id, {"authorised_users": updated_users})
    #
    #     return result is not None and result[0] > 0


