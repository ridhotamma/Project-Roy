from fastapi import APIRouter, Query
from app.models.user_ig_schedule import UserIGSchedule
from app.models.common import PaginatedResponse
from app.crud import user_ig_schedule as crud_schedule

router = APIRouter()


@router.post("/ig-schedules", response_model=UserIGSchedule)
async def create_schedule(schedule: UserIGSchedule):
    return crud_schedule.create_schedule(schedule)


@router.get("/ig-schedules", response_model=PaginatedResponse)
def get_schedules(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), is_active=Query(False)):
    return crud_schedule.get_schedules(skip, limit, is_active)


@router.get("/ig-schedules/{id}", response_model=UserIGSchedule)
async def get_schedule(id: str):
    return crud_schedule.get_schedule(id)


@router.put("/ig-schedules/{id}", response_model=UserIGSchedule)
async def update_schedule(id: str, schedule: UserIGSchedule):
    return crud_schedule.update_schedule(id, schedule)


@router.delete("/ig-schedules/{id}", response_model=dict)
async def delete_schedule(id: str):
    return crud_schedule.delete_schedule(id)
