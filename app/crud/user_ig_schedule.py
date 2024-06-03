from pymongo.errors import DuplicateKeyError
from app.database import get_schedule_collection
from app.models.user_ig_schedule import UserIGSchedule
from app.models.common import PaginatedResponse, PaginationMetadata
from fastapi import HTTPException, status
from datetime import datetime, timezone


def create_schedule(schedule: UserIGSchedule):
    schedule_collection = get_schedule_collection()
    try:
        schedule_collection.insert_one(schedule.model_dump())
        return schedule
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Schedule already exists")


def get_schedules(skip: int = 0, limit: int = 10, is_active: bool = False) -> PaginatedResponse:
    now = datetime.now(timezone.utc)
    schedule_collection = get_schedule_collection()
    schedule_filter = {"scheduled_time": {"$gt": now}} if is_active else {}
    total = schedule_collection.count_documents(schedule_filter)
    user_schedules_cursor = schedule_collection.find(schedule_filter).skip(skip).limit(limit)
    user_schedules = [UserIGSchedule(**schedule) for schedule in user_schedules_cursor]
    current_page = skip // limit + 1
    metadata = PaginationMetadata(total=total, current_page=current_page, page_size=limit)

    return PaginatedResponse(metadata=metadata, data=user_schedules)


def get_schedule(id: str):
    schedule_collection = get_schedule_collection()
    schedule = schedule_collection.find_one({"id": id})
    if schedule:
        return UserIGSchedule(**schedule)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")


def update_schedule(id: str, schedule: UserIGSchedule):
    schedule_collection = get_schedule_collection()
    current_schedule = schedule_collection.find_one({"id": id})
    if not current_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")

    updated_fields = {}
    for key, value in schedule.model_dump(exclude_unset=True).items():
        if current_schedule.get(key) != value:
            updated_fields[key] = value

    if not updated_fields:
        return UserIGSchedule(**current_schedule)

    updated_fields["updated_at"] = datetime.now(timezone.utc)
    result = schedule_collection.update_one({"id": id}, {"$set": updated_fields})
    if result.matched_count:
        current_schedule.update(updated_fields)
        return UserIGSchedule(**current_schedule)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")


def delete_schedule(id: str):
    schedule_collection = get_schedule_collection()
    result = schedule_collection.delete_one({"id": id})
    if result.deleted_count:
        return {"detail": "Schedule deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
