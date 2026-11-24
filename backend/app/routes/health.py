from fastapi import APIRouter, HTTPException

from app.cache import ping_cache
from app.config import get_settings
from app.db import ping_db

router = APIRouter()


async def dependency_status() -> dict:
    try:
        await ping_db()
        await ping_cache()
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "error", "detail": str(exc)},
        ) from exc
    return {
        "status": "ok",
        "mongo": "ok",
        "redis": "ok",
        "env": get_settings().app_env,
    }


@router.get("/health")
async def health() -> dict:
    return await dependency_status()


@router.get("/api/health")
async def api_health() -> dict:
    return await dependency_status()
