from abc import ABC, abstractmethod


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
