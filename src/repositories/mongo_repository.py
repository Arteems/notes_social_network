import logging

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorCollection


class MongoRepository:

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    @staticmethod
    def __prepare_id(data: dict) -> dict:
        result_dict = data
        result_dict["id"] = str(data.get("_id"))
        del result_dict["_id"]
        return data

    async def get_by_id(self, id: str) -> dict | None:
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
            return self.__prepare_id(dict(result))
        return None  # Возвращаем None, если документ не найден

    async def get_user_by_username(self, username: str) -> dict | None:
        result = await self.collection.find_one({"username": username})
        if result is not None:
            return self.__prepare_id(dict(result))
        return None

    async def get_user_by_mail(self, mail: str) -> dict | None:
        result = await self.collection.find_one({"mail": mail})
        if result is not None:
            return self.__prepare_id(dict(result))
        return None

    async def update(self, id: str, new_data: dict) -> dict | None:
        """Обновление записи и проверка было ли совершено
        обновление. если в базе данных было совершено изменение
         хотябы одной записи, то возвращается обновленная запись с указанным id, иначе None
        """
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": new_data}
        )
        if result.modified_count > 0:
            return await self.get_by_id(id)
        return None

    async def create(self, data: dict) -> str:
        return str((await self.collection.insert_one(data)).inserted_id)

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
