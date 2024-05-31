from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from jose import JWTError

from app.auth.jwt import verify_token
from app.crud.auth_user import get_user_by_username
from app.config import SECRET_KEY, ALGORITHM

EXCLUDED_PATHS = [
    "/ping",
    "/api/v1/auth/token",
    "/api/v1/auth/refresh-token",
    "/docs",
    "/openapi.json",
]


async def auth_middleware(request: Request, call_next):
    if any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
        return await call_next(request)

    authorization: str = request.headers.get("Authorization")
    if not authorization:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "status_code": status.HTTP_403_FORBIDDEN,
                "message": "Authorization header missing",
            },
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "status_code": status.HTTP_403_FORBIDDEN,
                "message": "Invalid authentication scheme",
            },
        )

    try:
        username = verify_token(token, SECRET_KEY, ALGORITHM)
        user = get_user_by_username(username)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "status_code": status.HTTP_403_FORBIDDEN,
                    "message": "Invalid token or user not found",
                },
            )
        request.state.user = user
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "status_code": e.status_code,
                "message": e.detail,
            },
        )
    except JWTError:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "status_code": status.HTTP_403_FORBIDDEN,
                "message": "Invalid token",
            },
        )

    response = await call_next(request)
    return response
