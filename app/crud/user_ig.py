from pymongo.errors import DuplicateKeyError
from app.database import get_user_collection
from app.models.user_ig import UserIG
from fastapi import HTTPException

def create_user(user: UserIG):
    user_collection = get_user_collection()
    try:
        user_collection.insert_one(user.dict())
        return user
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Username already exists")

def get_user(username: str):
    user_collection = get_user_collection()
    user = user_collection.find_one({"username": username})
    if user:
        return UserIG(**user)
    raise HTTPException(status_code=404, detail="User not found")

def update_user(username: str, user: UserIG):
    user_collection = get_user_collection()
    result = user_collection.update_one({"username": username}, {"$set": user.dict()})
    if result.matched_count:
        return user
    raise HTTPException(status_code=404, detail="User not found")

def delete_user(username: str):
    user_collection = get_user_collection()
    result = user_collection.delete_one({"username": username})
    if result.deleted_count:
        return {"detail": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
