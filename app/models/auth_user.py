from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
import uuid


class AuthUser(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    profile_picture: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword",
                "profile_picture": "http://example.com/profile.jpg",
                "session": {
                    "uuids": {
                        "phone_id": "57d64c41-a916-3fa5-bd7a-3796c1dab122",
                        "uuid": "8aa373c6-f316-44d7-b49e-d74563f4a8f3",
                        "client_session_id": "6c296d0a-3534-4dce-b5aa-a6a6ab017443",
                        "advertising_id": "8dc88b76-dfbc-44dc-abbc-31a6f1d54b04",
                        "device_id": "android-e021b636049dc0e9",
                    },
                    "cookies": {},
                    "last_login": 1596069420.0000145,
                    "device_settings": {
                        "cpu": "h1",
                        "dpi": "640dpi",
                        "model": "h1",
                        "device": "RS988",
                        "resolution": "1440x2392",
                        "app_version": "117.0.0.28.123",
                        "manufacturer": "LGE/lge",
                        "version_code": "168361634",
                        "android_release": "6.0.1",
                        "android_version": 23,
                    },
                    "user_agent": "Instagram 117.0.0.28.123 Android (23/6.0.1; ...US; 168361634)",
                },
            }
        }


class AuthUserIn(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    profile_picture: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "secretpassword",
                "profile_picture": "http://example.com/profile.jpg",
            }
        }


class AuthUserOut(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    profile_picture: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "profile_picture": "http://example.com/profile.jpg",
            }
        }


class LoginResult(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
