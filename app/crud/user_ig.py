from pymongo.errors import DuplicateKeyError
from app.database import get_ig_user_collection
from app.models.user_ig import UserIG, UserIGOut, UserIGIn
from app.models.common import PaginatedResponse, PaginationMetadata
from fastapi import HTTPException, status


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
    users_result = [UserIGOut(**user) for user in users_cursor]
    metadata = PaginationMetadata(total=total, current_page=current_page, page_size=limit)

    return PaginatedResponse(metadata=metadata, data=users_result)


def get_user(username: str):
    user_collection = get_ig_user_collection()
    user = user_collection.find_one({"username": username})
    if user:
        return UserIG(**user)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def update_user(username: str, user: UserIGIn):
    user_collection = get_ig_user_collection()
    current_user = user_collection.find_one({"username": username})

    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    current_user_model = UserIGIn(**current_user)

    update_data = {}
    for field, value in user.model_dump(exclude_unset=True).items():
        if getattr(current_user_model, field) != value:
            update_data[field] = value

    if update_data:
        result = user_collection.update_one({"username": username}, {"$set": update_data})
        if result.matched_count:
            return user_collection.find_one({"username": username})

    return current_user


def delete_user(username: str):
    user_collection = get_ig_user_collection()
    result = user_collection.delete_one({"username": username})
    if result.deleted_count:
        return {"detail": "User deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
