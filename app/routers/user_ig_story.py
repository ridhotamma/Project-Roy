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


@router.get("/ig-stories/{id}", response_model=UserIGStory)
async def get_story(id: str):
    return crud_story.get_story(id)


@router.put("/ig-stories/{id}", response_model=UserIGStory)
async def update_story(id: str, story: UserIGStory):
    return crud_story.update_story(id, story)


@router.delete("/ig-stories/{id}", response_model=dict)
async def delete_story(id: str):
    return crud_story.delete_story(id)
