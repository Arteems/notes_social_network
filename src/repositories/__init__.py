from motor import motor_asyncio

from ..config import mongo_settings
from .factories import RepositoryFactory
from .mongo_repository import MongoRepository

client = motor_asyncio.AsyncIOMotorClient(mongo_settings.url)
db = client[mongo_settings.database_name]
notes_collection = db[mongo_settings.collections.NOTES.value]
users_collection = db[mongo_settings.collections.USERS.value]

notes_repository = RepositoryFactory.create_repository(notes_collection)
users_repository = RepositoryFactory.create_repository(users_collection)
