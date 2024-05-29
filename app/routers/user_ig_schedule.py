from fastapi import APIRouter, Query
from app.models.user_ig_schedule import UserIGSchedule, PaginatedResponse
from app.crud import user_ig_schedule as crud_schedule

router = APIRouter()


@router.post("/v1/schedules", response_model=UserIGSchedule)
async def create_schedule(schedule: UserIGSchedule):
    return crud_schedule.create_schedule(schedule)


@router.get("/v1/schedules", response_model=PaginatedResponse)
def get_schedules(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    return crud_schedule.get_schedules(skip, limit)


@router.get("/v1/schedules/{username}", response_model=UserIGSchedule)
async def get_schedule(username: str):
    return crud_schedule.get_schedule(username)


@router.put("/v1/schedules/{username}", response_model=UserIGSchedule)
async def update_schedule(username: str, schedule: UserIGSchedule):
    return crud_schedule.update_schedule(username, schedule)


@router.delete("/v1/schedules/{username}", response_model=dict)
async def delete_schedule(username: str):
    return crud_schedule.delete_schedule(username)
