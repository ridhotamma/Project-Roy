from datetime import datetime, timezone
from celery import Celery
from app.models.user_ig_schedule import UserIGSchedule
from app.tasks.tasks import post_instagram_content, post_instagram_story
from app.crud.user_ig_schedule import get_schedules

celery_app = Celery("tasks")


def schedule_task(user_schedule: UserIGSchedule):
    eta = user_schedule.scheduled_time - datetime.now(timezone.utc)
    if user_schedule.action_type == "post_content":
        post_instagram_content.apply_async(
            args=[user_schedule.username, user_schedule.scheduled_item.model_dump()],
            eta=eta,
        )
    elif user_schedule.action_type == "post_story":
        post_instagram_story.apply_async(
            args=[user_schedule.username, user_schedule.scheduled_item.model_dump()],
            eta=eta,
        )


def schedule_non_expired_tasks():
    non_expired_schedules = get_schedules(skip=0, limit=1000, is_active=True)
    for user_schedule in non_expired_schedules.data:
        schedule_task(user_schedule)
