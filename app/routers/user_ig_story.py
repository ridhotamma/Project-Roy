from fastapi import APIRouter
from app.models.user_ig_story import UserIGStory
from app.crud import user_ig_story as crud_story

router = APIRouter()

@router.post("/v1/stories", response_model=UserIGStory)
async def create_story(story: UserIGStory):
    return crud_story.create_story(story)

@router.get("/v1/stories/{username}", response_model=UserIGStory)
async def get_story(username: str):
    return crud_story.get_story(username)

@router.put("/v1/stories/{username}", response_model=UserIGStory)
async def update_story(username: str, story: UserIGStory):
    return crud_story.update_story(username, story)

@router.delete("/v1/stories/{username}", response_model=dict)
async def delete_story(username: str):
    return crud_story.delete_story(username)