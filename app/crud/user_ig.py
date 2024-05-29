from pymongo.errors import DuplicateKeyError
from app.database import get_user_collection
from app.models.user_ig import UserIG, PaginatedResponse, PaginationMetadata
from fastapi import HTTPException, status


def create_user(user: UserIG):
    user_collection = get_user_collection()

    existing_user = user_collection.find_one({"username": user.username})

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    try:
        user_collection.insert_one(user.model_dump())
        return user
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Username already exists")


def get_users(skip: int = 0, limit: int = 10) -> PaginatedResponse:
    user_collection = get_user_collection()
    total = user_collection.count_documents({})
    users_cursor = user_collection.find().skip(skip).limit(limit)
    users = [UserIG(**user) for user in users_cursor]
    current_page = skip // limit + 1

    metadata = PaginationMetadata(
        total=total, current_page=current_page, page_size=limit
    )

    return PaginatedResponse(metadata=metadata, data=users)


def get_user(username: str):
    user_collection = get_user_collection()
    user = user_collection.find_one({"username": username})
    if user:
        return UserIG(**user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def update_user(username: str, user: UserIG):
    user_collection = get_user_collection()
    result = user_collection.update_one({"username": username}, {"$set": user.dict()})
    if result.matched_count:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def delete_user(username: str):
    user_collection = get_user_collection()
    result = user_collection.delete_one({"username": username})
    if result.deleted_count:
        return {"detail": "User deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
