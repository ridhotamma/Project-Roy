from fastapi import APIRouter
from app.models.user_ig_post import UserIGPost
from app.crud import user_ig_post as crud_post

router = APIRouter()

@router.post("/v1/posts", response_model=UserIGPost)
async def create_post(post: UserIGPost):
    return crud_post.create_post(post)

@router.get("/v1/posts/{username}", response_model=UserIGPost)
async def get_post(username: str):
    return crud_post.get_post(username)

@router.put("/v1/posts/{username}", response_model=UserIGPost)
async def update_post(username: str, post: UserIGPost):
    return crud_post.update_post(username, post)

@router.delete("/v1/posts/{username}", response_model=dict)
async def delete_post(username: str):
    return crud_post.delete_post(username)
