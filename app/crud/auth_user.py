from datetime import datetime, timezone, timedelta
from typing import Optional, Dict

from pymongo import ReturnDocument
from fastapi.exceptions import HTTPException
from fastapi import status
from app.auth.utils import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token
from app.models.auth_user import (
    AuthUserOut,
    AuthUserIn,
    PaginatedResponse,
    PaginationMetadata,
)
from app.database import get_auth_user_collection
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES


def create_user(user: AuthUserIn) -> AuthUserIn:
    user_collection = get_auth_user_collection()
    user.password = hash_password(user.password)
    user_collection.insert_one(user.model_dump())
    return user


def get_auth_users(skip: int, limit: int) -> PaginatedResponse:
    user_collection = get_auth_user_collection()
    total = user_collection.count_documents({})
    users_cursor = user_collection.find().skip(skip).limit(limit)
    users = [AuthUserOut(**user) for user in users_cursor]
    current_page = skip // limit + 1

    metadata = PaginationMetadata(
        total=total, current_page=current_page, page_size=limit
    )

    return PaginatedResponse(metadata=metadata, data=users)


def authenticate_user(username: str, password: str) -> Optional[Dict[str, str]]:
    user_collection = get_auth_user_collection()
    user = user_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return None
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user["username"]})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def get_user_by_username(username: str) -> Optional[AuthUserIn]:
    user_collection = get_auth_user_collection()
    user = user_collection.find_one({"username": username})
    if user:
        return AuthUserIn(**user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Auth User not found"
    )


def update_auth_user(username: str, user_update: AuthUserIn) -> Optional[AuthUserIn]:
    user_collection = get_auth_user_collection()
    user_update["updated_at"] = datetime.now(timezone.utc)
    updated_user = user_collection.find_one_and_update(
        {"username": username},
        {"$set": user_update},
        return_document=ReturnDocument.AFTER,
    )
    if updated_user:
        return AuthUserIn(**updated_user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with username '{username}' not found.",
    )


def delete_auth_user(username: str):
    auth_user_collection = get_auth_user_collection()
    result = auth_user_collection.delete_one({"username": username})
    if result.deleted_count:
        return {"detail": "User deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Auth user Not Found"
    )
