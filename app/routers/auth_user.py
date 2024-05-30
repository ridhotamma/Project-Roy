from datetime import timedelta
from typing import Dict, Annotated

from fastapi import APIRouter, HTTPException, status, Depends, Header, Query
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.jwt import verify_token, create_access_token
from app.models.auth_user import AuthUserIn, LoginResult, AuthUserOut, PaginatedResponse
from app.crud.auth_user import (
    create_user,
    authenticate_user,
    get_user_by_username,
    update_auth_user,
    get_auth_users,
)
from app.config import SECRET_KEY, ALGORITHM
from app.logger.utils import logger

router = APIRouter()


@router.post("/register/", response_model=AuthUserOut)
def register_user(user: AuthUserIn):
    return create_user(user)


@router.post("/token/", response_model=LoginResult)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    logger.info(f"User Login with {form_data.username} {form_data.password}")
    credentials = authenticate_user(form_data.username, form_data.password)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials


@router.post("/refresh-token/", response_model=Dict[str, str])
async def refresh_access_token(refresh_token: str = Header(...)):
    username = verify_token(refresh_token)
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/", response_model=PaginatedResponse)
async def get_users(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    return get_auth_users(skip, limit)


@router.get("/users/{username}", response_model=AuthUserOut)
async def get_user_detail(username: str):
    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )
    return user


@router.put("/users/{username}", response_model=PaginatedResponse)
async def update_user(username: str, user: AuthUserIn):
    return update_auth_user(username, user)


@router.get("/me/", response_model=AuthUserOut)
def read_users_me(token: str = Header(...)):
    username = verify_token(token, SECRET_KEY, ALGORITHM)
    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user
