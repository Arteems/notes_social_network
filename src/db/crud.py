from motor.motor_asyncio import AsyncIOMotorCollection
from src.db.collections import notes_collection


async def create_document(collection: AsyncIOMotorCollection, document: dict) -> str:
    result = await collection.insert_one(document)
    return repr(result.inserted_id)


async def get_document(collection: AsyncIOMotorCollection, id: int) -> dict:
    document = await collection.find_one({"_id": id})
    return document


async def get_all_documents(collection: AsyncIOMotorCollection) -> list[dict]:
    documents = await collection.find().to_list(length=None)
    return documents


async def update_document(
    collection: AsyncIOMotorCollection, id: int, update_data: dict
) -> int:
    result = await collection.update_one({"_id": id}, {"$set": update_data})
    return result.modified_count


async def delete_document(collection: AsyncIOMotorCollection, id: int) -> int:
    result = await collection.delete_one({"_id": id})
    return result.deleted_count
