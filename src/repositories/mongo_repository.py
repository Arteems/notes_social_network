from src.repositories.repository import Repository

from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId
from typing import Any, Dict
import logging


class MongoRepository(Repository):

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get(self, id: str) -> Dict[str, Any] | None:
        try:
            # Попытка найти документ по ID
            result = await self.collection.find_one({"_id": ObjectId(id)})
        except InvalidId:
            # Возвращаем None, если ID некорректный
            return None
        except Exception as e:
            # Логируем другие возможные ошибки
            logging.error(f"Ошибка при получении документа: {e}")
            return None

        if result:
            # Преобразуем результат в словарь, если это необходимо
            result_dict = dict(result)  # Преобразуем Mapping в dict
            result_dict["id"] = str(id)  # Используем id в строковом формате
            del result_dict["_id"]
            return result_dict

        return None  # Возвращаем None, если документ не найден

    async def update(self, id: str, new_data: dict) -> dict | None:
        """Обновление записи и проверка было ли совершено
        обновление. если в базе данных было совершено изменение
         хотябы одной записи, то возвращается обновленная запись с указанным id, иначе None
        """
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
