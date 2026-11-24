from fastapi import APIRouter
from pydantic import BaseModel, Field
from redis import Redis
from rq import Queue

from app.config import get_settings
from app.db import get_db
from app.tasks import sample_job

router = APIRouter()


class JobRequest(BaseModel):
    message: str = Field(default="hello from the template", min_length=1, max_length=500)


def get_queue() -> Queue:
    connection = Redis.from_url(get_settings().redis_url)
    return Queue("default", connection=connection)


@router.get("/api/jobs")
async def list_jobs() -> dict:
    cursor = get_db().jobs.find().sort("created_at", -1).limit(50)
    jobs = []
    async for document in cursor:
        created_at = document.get("created_at")
        jobs.append(
            {
                "id": str(document["_id"]),
                "job_id": document.get("job_id"),
                "message": document.get("message"),
                "created_at": created_at.isoformat() if created_at is not None else None,
            }
        )
    return {"jobs": jobs}


@router.post("/api/jobs")
def enqueue_job(body: JobRequest) -> dict:
    job = get_queue().enqueue(sample_job, body.message)
    status = job.get_status()
    status_value = status.value if hasattr(status, "value") else str(status)
    return {"job_id": job.id, "status": status_value}
