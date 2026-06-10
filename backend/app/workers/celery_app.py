from celery import Celery
from ..config import config

celery_app = Celery(
    "veluna",
    broker=config.REDIS_URL,
    backend=config.REDIS_URL,
    include=["app.workers.generation_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=60,
    task_soft_time_limit=50,
)