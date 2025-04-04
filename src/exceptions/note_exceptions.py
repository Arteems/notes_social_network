from fastapi import HTTPException, status


class NoteNotFoundError(HTTPException):
    def __init__(self, note_id: str):
        super().__init__(
            status.HTTP_404_NOT_FOUND, detail=f"Заметка {note_id} не найдена"
        )


class NoteCreateError(HTTPException):
    def __init__(self, note_title: str):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка создания заметки {note_title}",
        )


class NoteUpdateError(HTTPException):
    def __init__(self, user_id: str, note_id: str):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка обновления заметки {note_id} у пользователя {user_id}",
        )


class NoteDeleteError(HTTPException):
    def __init__(self, note_id: str):
        super().__init__(
            status.HTTP_400_BAD_REQUEST, detail=f"Заметка {note_id} не найдена"
        )
