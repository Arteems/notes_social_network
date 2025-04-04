from enum import Enum
import os

from pydantic import BaseModel

from pydantic import BaseModel


class Collections(Enum):
    NOTES = "notes"
    USERS = "users"


class MongoSettings(BaseModel):
    url: str = os.getenv("MONGO_URL")
    collections: Collections = Collections.NOTES
    database_name: str = "NotesSocialNetwork"


mongo_settings = MongoSettings()
