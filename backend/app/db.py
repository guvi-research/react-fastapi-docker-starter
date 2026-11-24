from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import get_settings

_client: AsyncIOMotorClient | None = None


def get_db() -> AsyncIOMotorDatabase:
    if _client is None:
        raise RuntimeError("Database is not connected")
    return _client[get_settings().mongo_db]


async def connect_db() -> None:
    global _client
    _client = AsyncIOMotorClient(get_settings().mongo_uri)
    await _client.admin.command("ping")


async def close_db() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


async def ping_db() -> None:
    if _client is None:
        raise RuntimeError("Database is not connected")
    await _client.admin.command("ping")
