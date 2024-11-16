from pydantic import BaseModel


class Editor(BaseModel):
    id: int


class Viewer(BaseModel):
    id: int


class Note(BaseModel):
    id: int
    title: str
    authorised_users: list[Editor, Viewer]
