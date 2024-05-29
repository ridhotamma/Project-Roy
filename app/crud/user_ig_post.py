from pymongo.errors import DuplicateKeyError
from app.database import get_post_collection
from app.models.user_ig_post import UserIGPost, PaginatedResponse, PaginationMetadata
from fastapi import HTTPException


def create_post(post: UserIGPost):
    post_collection = get_post_collection()
    try:
        post_collection.insert_one(post.dict())
        return post
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Post already exists")


def get_stories(skip: int = 0, limit: int = 10) -> PaginatedResponse:
    story_collection = get_post_collection()
    total = story_collection.count_documents({})
    user_posts_cursor = story_collection.find().skip(skip).limit(limit)
    user_posts = [UserIGPost(**post) for post in user_posts_cursor]
    current_page = skip // limit + 1

    metadata = PaginationMetadata(
        total=total, current_page=current_page, page_size=limit
    )

    return PaginatedResponse(metadata=metadata, data=user_posts)


def get_post(username: str):
    post_collection = get_post_collection()
    post = post_collection.find_one({"username": username})
    if post:
        return UserIGPost(**post)
    raise HTTPException(status_code=404, detail="Post not found")


def update_post(username: str, post: UserIGPost):
    post_collection = get_post_collection()
    result = post_collection.update_one({"username": username}, {"$set": post.dict()})
    if result.matched_count:
        return post
    raise HTTPException(status_code=404, detail="Post not found")


def delete_post(username: str):
    post_collection = get_post_collection()
    result = post_collection.delete_one({"username": username})
    if result.deleted_count:
        return {"detail": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")
