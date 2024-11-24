

class NoteNotFoundError(Exception):
    def __init__(self, note_id: str):
        super().__init__(f"заметка с ID {note_id} не найдена")
        self.note_id = note_id


class NoteCreateError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NoteUpdateError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NoteDeleteError(Exception):
    def __init__(self, message: str):
        super().__init__(message)