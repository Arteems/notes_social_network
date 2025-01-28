class NoteNotFoundError(Exception):
    def __init__(self, note_id: str):
        super().__init__(f"Заметка {note_id} не найдена")


class NoteCreateError(Exception):
    def __init__(self, user_id: str, note_title: str):
        super().__init__(
            f"Ошибка создания заметки {note_title} у пользователя {user_id}"
        )


class NoteUpdateError(Exception):
    def __init__(self, user_id: str, note_id: str):
        super().__init__(
            f"Ошибка обновления заметки {note_id} у пользователя {user_id}"
        )


class NoteDeleteError(Exception):
    def __init__(self, note_id: str):
        super().__init__(f"Заметка {note_id} не найдена")
