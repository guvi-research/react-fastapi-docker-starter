from redis.asyncio import Redis

from app.config import get_settings

_cache: Redis | None = None


def get_cache() -> Redis:
    if _cache is None:
        raise RuntimeError("Cache is not connected")
    return _cache


async def connect_cache() -> None:
    global _cache
    _cache = Redis.from_url(get_settings().cache_url, decode_responses=True)
    await _cache.ping()


async def close_cache() -> None:
    global _cache
    if _cache is not None:
        await _cache.aclose()
        _cache = None


async def ping_cache() -> None:
    if _cache is None:
        raise RuntimeError("Cache is not connected")
    await _cache.ping()
