from abc import ABC, abstractmethod
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.schemas.note import Editor, Viewer


class Repository(ABC):

    @abstractmethod
    async def get(self, id: str) -> dict | None:
        pass

    @abstractmethod
    async def update(self, id: str, new_data: dict) -> dict | None:
        pass

    @abstractmethod
    async def create(self, data: dict) -> str:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass


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




# class MySqlRepository(Repository):
#
#     async def get(self, id: str):
#         pass
#
#     async def update(self, id: str, new_data: dict):
#         pass
#
#     async def create(self, data: dict):
#         pass
#
#     async def delete(self, id: str):
#         pass


# class Factory(ABC):
#
#     @abstractmethod
#     def create_repository(self) -> Repository:
#         pass
#
#
# class RepositoryFactory(Factory):
#
#     def create_repository(self, storage) -> Repository:
#         if isinstance(storage, AsyncIOMotorCollection):
#             return MongoRepository(storage)
#         else:
#             raise TypeError
