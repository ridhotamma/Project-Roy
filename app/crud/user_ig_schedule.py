from pymongo.errors import DuplicateKeyError
from app.database import get_schedule_collection
from app.models.user_ig_schedule import (
    UserIGSchedule,
    PaginatedResponse,
    PaginationMetadata,
)
from fastapi import HTTPException


def create_schedule(schedule: UserIGSchedule):
    schedule_collection = get_schedule_collection()
    try:
        schedule_collection.insert_one(schedule.model_dump())
        return schedule
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Schedule already exists")


def get_schedules(skip: int = 0, limit: int = 10) -> PaginatedResponse:
    schedule_collection = get_schedule_collection()
    total = schedule_collection.count_documents({})
    user_schedules_cursor = schedule_collection.find().skip(skip).limit(limit)
    user_schedules = [UserIGSchedule(**schedule) for schedule in user_schedules_cursor]

    current_page = skip // limit + 1

    metadata = PaginationMetadata(
        total=total, current_page=current_page, page_size=limit
    )

    return PaginatedResponse(metadata=metadata, data=user_schedules)


def get_schedule(username: str):
    schedule_collection = get_schedule_collection()
    schedule = schedule_collection.find_one({"username": username})
    if schedule:
        return UserIGSchedule(**schedule)
    raise HTTPException(status_code=404, detail="Schedule not found")


def update_schedule(username: str, schedule: UserIGSchedule):
    schedule_collection = get_schedule_collection()
    result = schedule_collection.update_one(
        {"username": username}, {"$set": schedule.model_dump()}
    )
    if result.matched_count:
        return schedule
    raise HTTPException(status_code=404, detail="Schedule not found")


def delete_schedule(username: str):
    schedule_collection = get_schedule_collection()
    result = schedule_collection.delete_one({"username": username})
    if result.deleted_count:
        return {"detail": "Schedule deleted"}
    raise HTTPException(status_code=404, detail="Schedule not found")
