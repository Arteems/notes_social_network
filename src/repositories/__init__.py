from motor import motor_asyncio

from config import mongo_settings
from .mongo_repository import MongoRepository

client = motor_asyncio.AsyncIOMotorClient(mongo_settings.url)
db = client[mongo_settings.database_name]
notes_collection = db["notes"]
users_collection = db["users"]

notes_repository = MongoRepository(notes_collection)
users_repository = MongoRepository(users_collection)
