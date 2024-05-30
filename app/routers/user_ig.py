from fastapi import APIRouter, Query
from app.models.user_ig import UserIG, UserIGOut, PaginatedResponse
from app.crud import user_ig as crud_user

router = APIRouter()


@router.get("/ig-users/", response_model=PaginatedResponse)
def get_instagram_users(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    return crud_user.get_users(skip, limit)


@router.post("/ig-users/", response_model=UserIG)
async def create_instagram_user(user: UserIG):
    return crud_user.create_user(user)


@router.get("/ig-users/{username}", response_model=UserIGOut)
async def get_instagram_user(username: str):
    return crud_user.get_user(username)


@router.put("/ig-users/{username}", response_model=UserIGOut)
async def update_instagram_user(username: str, user: UserIG):
    return crud_user.update_user(username, user)


@router.delete("/ig-users/{username}", response_model=dict)
async def delete_instagram_user(username: str):
    return crud_user.delete_user(username)
