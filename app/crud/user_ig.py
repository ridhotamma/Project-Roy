from pymongo.errors import DuplicateKeyError
from app.database import get_ig_user_collection
from app.models.user_ig import UserIG, UserIGOut, PaginatedResponse, PaginationMetadata
from fastapi import HTTPException, status
from pymongo import ReturnDocument
from datetime import datetime, timezone


def create_user(user: UserIG):
    user_collection = get_ig_user_collection()

    existing_user = user_collection.find_one({"username": user.username})

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    try:
        user_collection.insert_one(user.model_dump())
        return user
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Username already exists")


def get_users(skip: int = 0, limit: int = 10) -> PaginatedResponse:
    user_collection = get_ig_user_collection()
    total = user_collection.count_documents({})
    users_cursor = user_collection.find().skip(skip).limit(limit)
    current_page = skip // limit + 1

    users_result = []
    for user in users_cursor:
        user["id"] = user.pop("_id")
        users_result.append(user)

    metadata = PaginationMetadata(
        total=total, current_page=current_page, page_size=limit
    )

    return PaginatedResponse(metadata=metadata, data=users_result)


def get_user(username: str):
    user_collection = get_ig_user_collection()
    user = user_collection.find_one({"username": username})
    if user:
        user["id"] = user.pop("_id")
        return UserIG(**user)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def update_user(username: str, user: UserIGOut):
    user_collection = get_ig_user_collection()
    result = user_collection.update_one({"username": username}, {"$set": user.dict()})
    if result.matched_count:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def delete_user(username: str):
    user_collection = get_ig_user_collection()
    result = user_collection.delete_one({"username": username})
    if result.deleted_count:
        return {"detail": "User deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def update_user_session(username: str, session_data: dict):
    user_collection = get_ig_user_collection()
    session = {
        "uuids": session_data.get("uuids", {}),
        "cookies": session_data.get("cookies", {}),
        "last_login": session_data.get(
            "last_login", datetime.now(timezone.utc).timestamp()
        ),
        "device_settings": session_data.get("device_settings", {}),
        "user_agent": session_data.get("user_agent", ""),
    }
    update_data = {"session": session, "updated_at": datetime.now(timezone.utc)}

    updated_user = user_collection.find_one_and_update(
        {"username": username},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found.",
        )
    return updated_user
