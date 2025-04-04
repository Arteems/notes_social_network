import os

from pydantic import BaseModel


class MongoSettings(BaseModel):
    url: str = os.getenv("MONGO_URL")
    database_name: str = "NotesSocialNetwork"


mongo_settings = MongoSettings()
