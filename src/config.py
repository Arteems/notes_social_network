from enum import Enum

from pydantic import BaseModel


class Collections(Enum):
    NOTES = "notes"
    USERS = "users"


class MongoSettings(BaseModel):
    url: str = "mongodb://localhost:27017"
    collections: Collections = Collections.NOTES
    database_name: str = "NotesSocialNetwork"


mongo_settings = MongoSettings()
