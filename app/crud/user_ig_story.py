from pymongo.errors import DuplicateKeyError
from app.database import get_story_collection
from app.models.user_ig_story import UserIGStory
from fastapi import HTTPException

def create_story(story: UserIGStory):
    story_collection = get_story_collection()
    try:
        story_collection.insert_one(story.dict())
        return story
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Story already exists")

def get_story(username: str):
    story_collection = get_story_collection()
    story = story_collection.find_one({"username": username})
    if story:
        return UserIGStory(**story)
    raise HTTPException(status_code=404, detail="Story not found")

def update_story(username: str, story: UserIGStory):
    story_collection = get_story_collection()
    result = story_collection.update_one({"username": username}, {"$set": story.dict()})
    if result.matched_count:
        return story
    raise HTTPException(status_code=404, detail="Story not found")

def delete_story(username: str):
    story_collection = get_story_collection()
    result = story_collection.delete_one({"username": username})
    if result.deleted_count:
        return {"detail": "Story deleted"}
    raise HTTPException(status_code=404, detail="Story not found")
