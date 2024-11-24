from pydantic import BaseModel, ConfigDict


class Editor(BaseModel):
    id: str


class Viewer(BaseModel):
    id: str


class Note(BaseModel):
    id: str
    title: str
    content: str
    editors: list[Editor]
    viewers: list[Viewer]


class UpdateNote(BaseModel):
    title: str | None = None
    content: str | None = None
    editors: list[Editor] | None = None
    viewers: list[Viewer] | None = None





