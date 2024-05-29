from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class AuthUser(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    profile_picture: Optional[str] = None

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword",
                "profile_picture": "http://example.com/profile.jpg",
            }
        }


class AuthUserOut(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    profile_picture: Optional[str] = None

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "profile_picture": "http://example.com/profile.jpg",
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str


class PaginationMetadata(BaseModel):
    total: int
    current_page: int
    page_size: int


class PaginatedResponse(BaseModel):
    metadata: PaginationMetadata
    data: List[AuthUserOut]
