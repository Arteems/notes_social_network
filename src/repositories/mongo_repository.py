from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from repository import Repository



class MongoRepository(Repository):

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get(self, id: str) -> dict | None:
        result = await self.collection.find_one({"_id": ObjectId(id)})
        return result if result else None

    async def update(self, id: str, new_data: dict) -> dict | None:
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": new_data}
        )
        return result if result else None

    async def create(self, data: dict) -> str:
        return str((await self.collection.insert_one(data)).inserted_id)

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0


