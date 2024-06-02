from datetime import datetime, timezone
from celery import shared_task
from app.models.user_ig_schedule import UserIGSchedule
from app.tasks.instagram_tasks import post_content_to_instagram, post_story_to_instagram
from app.database import get_ig_user_collection


@shared_task
def check_and_process_schedules():
    schedules_collection = get_ig_user_collection()
    now = datetime.now(timezone.utc)
    unprocessed_schedules = schedules_collection.find({"status_type": "unprocessed", "scheduled_time": {"$lte": now}})

    for schedule in unprocessed_schedules:
        schedule_obj = UserIGSchedule(**schedule)
        if schedule_obj.scheduled_time < now:
            schedules_collection.update_one({"_id": schedule_obj.id}, {"$set": {"status_type": "expired"}})
        else:
            try:
                if schedule_obj.action_type == "post_content":
                    post_content_to_instagram(schedule_obj.scheduled_item)
                elif schedule_obj.action_type == "post_story":
                    post_story_to_instagram(schedule_obj.scheduled_item)

                schedules_collection.update_one({"_id": schedule_obj.id}, {"$set": {"status_type": "success"}})
            except Exception as e:
                schedules_collection.update_one(
                    {"_id": schedule_obj.id},
                    {"$set": {"status_type": "failed", "error": str(e)}},
                )
