from abc import ABC, abstractmethod
from motor.motor_asyncio import AsyncIOMotorCollection
from mongo_repository import MongoRepository
from repository import Repository


class Factory(ABC):

    @abstractmethod
    def create_repository(self) -> Repository:
        pass


class RepositoryFactory(Factory):

    def create_repository(self, storage) -> Repository:
        if isinstance(storage, AsyncIOMotorCollection):
            return MongoRepository(storage)
        raise TypeError