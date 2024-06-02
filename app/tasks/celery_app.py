from celery import Celery
from celery.schedules import crontab

celery_app = Celery("worker", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_concurrency=2,
    beat_schedule={
        "check-schedules-every-minute": {
            "task": "tasks.schedule_tasks.check_and_process_schedules",
            "schedule": crontab(minute="*/1"),
        },
    },
)
