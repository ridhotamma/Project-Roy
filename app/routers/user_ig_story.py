from fastapi import APIRouter, Query
from app.models.user_ig_story import UserIGStory, PaginatedResponse
from app.crud import user_ig_story as crud_story

router = APIRouter()


@router.post("/ig-stories", response_model=UserIGStory)
async def create_story(story: UserIGStory):
    return crud_story.create_story(story)


@router.get("/ig-stories", response_model=PaginatedResponse)
def get_stories(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    return crud_story.get_stories(skip, limit)


@router.get("/ig-stories/{username}", response_model=UserIGStory)
async def get_story(username: str):
    return crud_story.get_story(username)


@router.put("/ig-stories/{username}", response_model=UserIGStory)
async def update_story(username: str, story: UserIGStory):
    return crud_story.update_story(username, story)


@router.delete("/ig-stories/{username}", response_model=dict)
async def delete_story(username: str):
    return crud_story.delete_story(username)
