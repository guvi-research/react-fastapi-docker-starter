import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.cache import close_cache, connect_cache
from app.config import get_settings
from app.db import close_db, connect_db
from app.routes.health import router as health_router
from app.routes.jobs import router as jobs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
    await connect_db()
    await connect_cache()
    yield
    await close_cache()
    await close_db()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Quick Project Setup", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    app.include_router(jobs_router)
    return app


app = create_app()
