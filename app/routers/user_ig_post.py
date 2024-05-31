from fastapi import APIRouter, Query
from app.models.user_ig_post import UserIGPost
from app.models.common import PaginatedResponse
from app.crud import user_ig_post as crud_post

router = APIRouter()


@router.post("/ig-posts", response_model=UserIGPost)
async def create_post(post: UserIGPost):
    return crud_post.create_post(post)


@router.get("/ig-posts", response_model=PaginatedResponse)
def get_posts(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    return crud_post.get_posts(skip, limit)


@router.get("/ig-posts/{id}", response_model=UserIGPost)
async def get_post(id: str):
    return crud_post.get_post(id)


@router.put("/ig-posts/{id}", response_model=UserIGPost)
async def update_post(id: str, post: UserIGPost):
    return crud_post.update_post(id, post)


@router.delete("/ig-posts/{id}", response_model=dict)
async def delete_post(id: str):
    return crud_post.delete_post(id)
