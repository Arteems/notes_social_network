from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MONGO_")
    url: str = "mongodb://mongo:27017"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")
    host: str = "redis"
    port: int = 6379
    db: int = 0


class DataBaseSettings(BaseSettings):
    mongo: MongoSettings = MongoSettings()
    redis: RedisSettings = RedisSettings()


class TelegramSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TELEGRAM_")
    token: SecretStr


class Settings(BaseSettings):
    telegram: TelegramSettings = TelegramSettings()
    database: DataBaseSettings = DataBaseSettings()


settings = Settings()
