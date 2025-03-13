import redis.asyncio as redis
from config import settings


class RedisClient:
    """Асинхронный клиент Redis для хранения и проверки сессий."""

    def __init__(self) -> None:
        self.client = redis.Redis(
            host=settings.database.redis.host,
            port=settings.database.redis.port,
            db=settings.database.redis.db,
            decode_responses=True,
        )

    async def set_session(self, session: str, value: str, ttl: int) -> None:
        """Сохранить токен в Redis с временем жизни (TTL)."""
        await self.client.setex(session, ttl, value)

    async def get_value_by_token(self, session: str) -> str | None:
        """Получить user_id по session, если он есть в Redis."""
        return await self.client.get(session)

    async def revoke_session(self, session: str) -> None:
        """Удалить session из Redis (отзыв session)."""
        await self.client.delete(session)


redis_client = RedisClient()
