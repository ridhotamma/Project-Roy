from pymongo.errors import DuplicateKeyError
from app.database import get_schedule_collection
from app.models.user_ig_schedule import UserIGSchedule
from fastapi import HTTPException

def create_schedule(schedule: UserIGSchedule):
    schedule_collection = get_schedule_collection()
    try:
        schedule_collection.insert_one(schedule.dict())
        return schedule
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Schedule already exists")

def get_schedule(username: str):
    schedule_collection = get_schedule_collection()
    schedule = schedule_collection.find_one({"username": username})
    if schedule:
        return UserIGSchedule(**schedule)
    raise HTTPException(status_code=404, detail="Schedule not found")

def update_schedule(username: str, schedule: UserIGSchedule):
    schedule_collection = get_schedule_collection()
    result = schedule_collection.update_one({"username": username}, {"$set": schedule.dict()})
    if result.matched_count:
        return schedule
    raise HTTPException(status_code=404, detail="Schedule not found")

def delete_schedule(username: str):
    schedule_collection = get_schedule_collection()
    result = schedule_collection.delete_one({"username": username})
    if result.deleted_count:
        return {"detail": "Schedule deleted"}
    raise HTTPException(status_code=404, detail="Schedule not found")
