from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.repositories.repository import Repository


class MongoRepository(Repository):

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get(self, id: str) -> dict | None:
        result = await self.collection.find_one({"_id": ObjectId(id)})
        if result:
            result["id"] = id
            del result["_id"]
            return result
        return None

    async def update(self, id: str, new_data: dict) -> dict | None:
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": new_data}
        )
        if result.modified_count > 0:
            return await self.get(id)
        return None

    async def create(self, data: dict) -> str:
        return str((await self.collection.insert_one(data)).inserted_id)

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
