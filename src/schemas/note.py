from pydantic import BaseModel


class UpdateNote(BaseModel):
    title: str | None = None
    content: str | None = None
    editors: list[str] | None = None
    viewers: list[str | None] | None = None
    owner_id: str | None = None


class CreateNote(BaseModel):
    title: str = "Без названия"
    content: str = ""
    editors: list[str]
    viewers: list[str | None] = []
    owner_id: str


class Note(CreateNote):
    id: str
