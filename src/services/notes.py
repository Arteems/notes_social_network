from ..repositories.repository import Repository
from ..schemas.note import Note, UpdateNote, CreateNote
from ..exceptions.exceptions import (
    NoteUpdateError,
    NoteCreateError,
    NoteDeleteError,
    NoteNotFoundError,
)


class NoteService:
    def __init__(self, repository: Repository):
        self.repository = repository

    # async def __note_exist(self, note_id: str):
    #     existing_note = await self.repository.get(note_id)
    #     if not existing_note:
    #         raise NoteNotFoundError(note_id)
    #     print(f"Заметка {note_id} существует")

    async def get(self, note_id: str) -> Note:
        existing_note = await self.repository.get(note_id)
        if not existing_note:
            raise NoteNotFoundError(note_id=note_id)
        return Note(**existing_note)

    async def create(self, note: CreateNote) -> str:
        try:
            result = await self.repository.create(note.model_dump())
            return result
        except Exception as e:
            raise NoteCreateError(user_id=note.id, note_title=note.title) from e

    async def update(self, note_id: str, new_data: UpdateNote) -> dict:
        note = await self.get(note_id)

        try:
            result = await self.repository.update(
                note_id, new_data.model_dump(exclude_unset=True)
            )
            return result
        except Exception as e:
            raise NoteUpdateError(note_id=note_id, user_id=note.owner_id) from e

    async def delete(self, note_id: str) -> bool:
        existing_note = await self.get(note_id)
        if not existing_note:
            raise NoteNotFoundError(note_id=note_id)

        try:
            result = await self.repository.delete(note_id)
            return result
        except Exception as e:
            raise NoteDeleteError(note_id=note_id) from e

    async def delete_viewer(self, note_id: str, viewer_id: str) -> bool:
        note = await self.repository.get(note_id)
        if not note:
            raise NoteNotFoundError(note_id=note_id)

        note = Note(**note)
        if viewer_id in note.viewers:
            note.viewers.remove(viewer_id)
            await self.repository.update(note_id, note.model_dump())
            return True
        return False

    async def delete_editor(self, note_id: str, editor_id: str) -> bool:
        note = await self.get(note_id)
        if not note:
            raise NoteNotFoundError(note_id)

        if editor_id in note.editors:
            note.editors.remove(editor_id)
            await self.repository.update(note_id, note.model_dump())
            return True
        return False

    async def add_viewer(self, note_id: str, viewer_id: str) -> bool:
        note = await self.get(note_id)
        if not note:
            raise NoteNotFoundError(note_id)

        if viewer_id in note.viewers:
            note.viewers.append(viewer_id)
            await self.repository.update(viewer_id, note.model_dump())
            return True
        return False

    async def add_editor(self, note_id: str, editor_id: str) -> bool:
        note = await self.get(note_id)
        if not note:
            raise NoteNotFoundError(note_id)

        if editor_id in note.editors:
            note.editors.append(editor_id)
            await self.repository.update(editor_id, note.model_dump())
            return True
        return False
