import jwt
from passlib.context import CryptContext
from app.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def encrypt_password(password: str) -> str:
    encoded_jwt = jwt.encode({"password": password}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decrypt_password(encoded_jwt: str) -> str:
    decoded_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_jwt["password"]
