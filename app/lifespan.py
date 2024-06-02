from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import get_auth_user_collection
from app.auth.utils import hash_password
from app.config import INITIAL_USER_USERNAME, INITIAL_USER_PASSWORD, INITIAL_USER_EMAIL
from app.models.auth_user import AuthUser


@asynccontextmanager
async def task_runner(app: FastAPI):
    auth_user_collection = get_auth_user_collection()

    existing_user = auth_user_collection.find_one(
        {
            "$and": [
                {"username": INITIAL_USER_USERNAME},
                {"password": hash_password(INITIAL_USER_PASSWORD)},
            ]
        }
    )

    if not existing_user:
        new_user = AuthUser(
            email=INITIAL_USER_EMAIL,
            username=INITIAL_USER_USERNAME,
            password=hash_password(INITIAL_USER_PASSWORD),
        )
        auth_user_collection.insert_one(new_user.model_dump())

    yield

    # Code to run at shutdown
    # (e.g., cleanup resources if needed)
