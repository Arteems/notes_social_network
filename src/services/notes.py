from ..repositories.notes import Repository
from ..schemas.note import Viewer, Editor


class NoteService:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def create(
        self,
        title: str,
        editors: list[int | None] = None,
        viewers: list[int | None] = None,
    ) -> str:
        note = {
            "title": title,
            "authorised_users": [],
        }
        if editors:
            note["authorised_users"].extend(
                [Editor(id=editor_id) for editor_id in editors]
            )
        if viewers:
            note["authorised_users"].extend(
                [Viewer(id=viewer_id) for viewer_id in viewers]
            )

        result = await self.repository.create(note)

        return result

    async def delete_viewer(self, note_id: str, viewer_id: int) -> bool:
        note = await self.repository.get(note_id)
        if not note:
            return False

        updated_users = [
            user
            for user in note['authorised_users']
            if not (isinstance(user, Viewer) and user.id == viewer_id)
        ]

        result = await self.repository.update(
            note_id, {'authorised_users': updated_users}
        )
        return result[0]

    async def delete_editor(self, note_id: str, editor_id: int):
        note = await self.repository.get(note_id)
        if not note:
            return False

        updated_users = [
            user
            for user in note['authorised_users']
            if not (isinstance(user, Editor) and user.id == editor_id)
        ]

        result = await self.repository.update(
            note_id, {'authorised_users': updated_users}
        )
        return result[0]



