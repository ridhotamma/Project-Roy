from fastapi import APIRouter
from app.models.user_ig import UserIG
from app.crud import user as crud_user

router = APIRouter()

@router.post("/v1/users", response_model=UserIG)
async def create_user(user: UserIG):
    return crud_user.create_user(user)

@router.get("/v1/users/{username}", response_model=UserIG)
async def get_user(username: str):
    return crud_user.get_user(username)

@router.put("/v1/users/{username}", response_model=UserIG)
async def update_user(username: str, user: UserIG):
    return crud_user.update_user(username, user)

@router.delete("/v1/users/{username}", response_model=dict)
async def delete_user(username: str):
    return crud_user.delete_user(username)
