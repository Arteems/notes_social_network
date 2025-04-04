import logging

from repositories import MongoRepository

from exceptions.note_exceptions import (
    NoteDeleteError,
    NoteNotFoundError,
    NoteUpdateError,
)
from schemas.note import CreateNote, Note, UpdateNote


class NoteService:
    def __init__(self, repository: MongoRepository):
        self.repository = repository

    async def get(self, note_id: str) -> Note:
        existing_note = await self.repository.get_by_id(note_id)
        if existing_note is None:
            raise NoteNotFoundError(note_id=note_id)
        return Note(**existing_note)

    async def create(self, note: CreateNote) -> str:
        try:
            return await self.repository.create(note.model_dump())
        except Exception as e:
            logging.error(f"Ошибка при создании заметки: {e}")
            raise AssertionError

    async def update(self, note_id: str, new_data: UpdateNote) -> Note:
        note = await self.get(note_id)
        try:
            result = await self.repository.update(
                note_id, new_data.model_dump(exclude_unset=True)
            )
            return Note(**result)
        except Exception:
            raise NoteUpdateError(note_id=note_id, user_id=note.owner_id)

    async def delete(self, note_id: str) -> bool:
        await self.get(note_id)
        try:
            return await self.repository.delete(note_id)
        except Exception:
            raise NoteDeleteError(note_id=note_id)

    async def delete_viewer(self, note_id: str, viewer_id: str) -> bool:
        note = await self.repository.get_by_id(note_id)
        note = Note(**note)
        if viewer_id in note.viewers:
            note.viewers.remove(viewer_id)
            await self.repository.update(
                note_id, note.model_dump(exclude_defaults=True)
            )
            return True
        return False

    async def delete_editor(self, note_id: str, editor_id: str) -> bool:
        note = await self.get(note_id)
        if editor_id in note.editors:
            note.editors.remove(editor_id)
            await self.repository.update(
                note_id, note.model_dump(exclude_defaults=True)
            )
            return True
        return False

    async def add_viewer(self, note_id: str, viewer_id: str) -> bool:
        note = await self.get(note_id)
        if viewer_id not in note.viewers:
            note.viewers.append(viewer_id)
            await self.repository.update(
                note_id, note.model_dump(exclude_defaults=True)
            )
            return True
        return False

    async def add_editor(self, note_id: str, editor_id: str) -> bool:
        note = await self.get(note_id)
        if editor_id not in note.editors:
            note.editors.append(editor_id)
            await self.repository.update(
                note_id, note.model_dump(exclude_defaults=True)
            )
            return True
        return False
