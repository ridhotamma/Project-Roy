from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.jwt import verify_token, create_access_token
from app.models.auth_user import AuthUser, Token, AuthUserOut
from app.crud.auth_user import create_user, authenticate_user, get_user_by_username
from app.config import SECRET_KEY, ALGORITHM

router = APIRouter()


@router.post("/register", response_model=AuthUserOut)
def register_user(user: AuthUser):
    return create_user(user)


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/refresh-token", response_model=Dict[str, str])
async def refresh_access_token(refresh_token: str = Header(...)):
    username = verify_token(refresh_token)
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=AuthUserOut)
def read_users_me(token: str = Header(...)):
    username = verify_token(token, SECRET_KEY, ALGORITHM)
    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user
