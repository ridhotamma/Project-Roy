# app/models/auth_user.py

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class AuthUser(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    created_at: datetime
    updated_at: datetime
    profile_picture: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "profile_picture": "http://example.com/profile.jpg",
            }
        }


class PaginationMetadata(BaseModel):
    total: int
    current_page: int
    page_size: int


class PaginatedResponse(BaseModel):
    metadata: PaginationMetadata
    data: List[AuthUser]
