from motor import motor_asyncio
from ..config import mongo_settings
from .mongo_repository import MongoRepository


client = motor_asyncio.AsyncIOMotorClient(mongo_settings.url)
notes_collection = client[mongo_settings.collections.NOTES.value]
users_collection = client[mongo_settings.collections.USERS.value]


notes_repository = MongoRepository(notes_collection)
users_repository = MongoRepository(users_collection)







