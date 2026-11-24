from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    app_env: str = "development"
    log_level: str = "info"
    mongo_uri: str = "mongodb://mongo:27017/app"
    mongo_db: str = "app"
    redis_url: str = "redis://redis:6379/0"
    cache_url: str = "redis://redis:6379/1"
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
