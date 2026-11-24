import logging
from datetime import datetime, timezone

from pymongo import MongoClient
from rq import get_current_job

from app.config import get_settings

logger = logging.getLogger(__name__)


def sample_job(message: str = "hello from the template") -> str:
    """Write one document so the worker, Redis, and MongoDB are proven together."""
    settings = get_settings()
    current = get_current_job()
    client = MongoClient(settings.mongo_uri)
    try:
        document = {
            "job_id": current.id if current is not None else None,
            "message": message,
            "created_at": datetime.now(timezone.utc),
        }
        result = client[settings.mongo_db].jobs.insert_one(document)
        inserted_id = str(result.inserted_id)
        logger.info("sample_job wrote %s", inserted_id)
        return inserted_id
    finally:
        client.close()
