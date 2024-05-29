from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.jwt import verify_token, SECRET_KEY, ALGORITHM
from app.models.auth_user import AuthUser, Token, AuthUserOut, LoginRequest
from app.crud.auth_user import create_user, authenticate_user, get_user_by_username

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=AuthUserOut)
def register_user(user: AuthUser):
    return create_user(user)


@router.post("/token", response_model=Token)
def login_for_access_token(payload: LoginRequest):
    user = authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get("/users/me", response_model=AuthUserOut)
def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token, SECRET_KEY, ALGORITHM)
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user
