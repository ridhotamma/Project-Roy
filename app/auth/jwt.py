from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi.exceptions import HTTPException
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM) -> str:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError()
        return username
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
