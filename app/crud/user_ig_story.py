from pymongo.errors import DuplicateKeyError
from app.database import get_story_collection
from app.models.user_ig_story import UserIGStory
from app.models.common import PaginatedResponse, PaginationMetadata
from fastapi import HTTPException, status
from datetime import datetime, timezone


def create_story(story: UserIGStory):
    story_collection = get_story_collection()
    try:
        story_collection.insert_one(story.model_dump())
        return story
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Story already exists")


def get_stories(skip: int = 0, limit: int = 10) -> PaginatedResponse:
    story_collection = get_story_collection()
    total = story_collection.count_documents({})
    user_stories_cursor = story_collection.find().skip(skip).limit(limit)
    user_stories = [UserIGStory(**story) for story in user_stories_cursor]
    current_page = skip // limit + 1

    metadata = PaginationMetadata(total=total, current_page=current_page, page_size=limit)

    return PaginatedResponse(metadata=metadata, data=user_stories)


def get_story(id: str):
    story_collection = get_story_collection()
    story = story_collection.find_one({"id": id})
    if story:
        return UserIGStory(**story)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")


def update_story(id: str, story: UserIGStory):
    story_collection = get_story_collection()
    current_story = story_collection.find_one({"id": id})
    if not current_story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    updated_fields = {}
    for key, value in story.model_dump(exclude_unset=True).items():
        if current_story.get(key) != value:
            updated_fields[key] = value

    if not updated_fields:
        return UserIGStory(**current_story)

    updated_fields["updated_at"] = datetime.now(timezone.utc)
    result = story_collection.update_one({"id": id}, {"$set": updated_fields})
    if result.matched_count:
        current_story.update(updated_fields)
        return UserIGStory(**current_story)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")


def delete_story(id: str):
    story_collection = get_story_collection()
    result = story_collection.delete_one({"id": id})
    if result.deleted_count:
        return {"detail": "Story deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
