from fastapi import Request, HTTPException, status
from jose import JWTError

from app.auth.jwt import verify_token
from app.crud.auth_user import get_user_by_username
from app.config import SECRET_KEY, ALGORITHM


async def auth_middleware(request: Request, call_next):
    authorization: str = request.headers.get("Authorization")
    if authorization:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme",
            )
        try:
            username = verify_token(token, SECRET_KEY, ALGORITHM)
            user = get_user_by_username(username)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or user not found",
                )
            request.state.user = user
        except HTTPException as e:
            raise e
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
    else:
        request.state.user = None

    response = await call_next(request)
    return response
