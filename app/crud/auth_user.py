from datetime import datetime
from pymongo import ReturnDocument
from app.auth.utils import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.models.auth_user import AuthUser
from app.database import get_user_collection
from typing import Optional, Dict

def create_user(user: AuthUser) -> AuthUser:
    user_collection = get_user_collection()
    user.password = hash_password(user.password)
    user.created_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()
    user_collection.insert_one(user.dict())
    return user

def authenticate_user(username: str, password: str) -> Optional[Dict[str, str]]:
    user_collection = get_user_collection()
    user = user_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return None
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_user_by_username(username: str) -> Optional[AuthUser]:
    user_collection = get_user_collection()
    user = user_collection.find_one({"username": username})
    if user:
        return AuthUser(**user)
    return None

def update_user(username: str, user_update: Dict) -> Optional[AuthUser]:
    user_collection = get_user_collection()
    updated_user = user_collection.find_one_and_update(
        {"username": username},
        {"$set": user_update},
        return_document=ReturnDocument.AFTER
    )
    if updated_user:
        return AuthUser(**updated_user)
    return None
