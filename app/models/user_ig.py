from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Annotated
from fastapi import Form
from app.models.common import PyObjectId


class Session(BaseModel):
    uuids: Dict[str, str]
    cookies: Dict[str, Any] = {}
    last_login: float
    device_settings: Dict[str, Any]
    user_agent: str

    class Config:
        json_schema_extra = {
            "example": {
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
            }
        }


class UserIG(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    proxy_url: Optional[str] = Field(None, pattern=r"^http://.*|https://.*")
    session: Optional[Session] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword",
                "proxy_url": "http://proxy.example.com:8080",
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


class UserIGOut(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    proxy_url: Optional[str] = Field(None, pattern=r"^http://.*|https://.*")
    session: Optional[Session] = None


class LoginRequest(BaseModel):
    username: Annotated[str, Form()]
    password: Annotated[str, Form()]


class CreateStoryRequest(BaseModel):
    username: Annotated[str, Form()]
    photo_path: Annotated[str, Form()]


class CreatePostRequest(BaseModel):
    username: Annotated[str, Form()]
    photo_path: Annotated[str, Form()]
    caption: Annotated[str, Form()]


class CreateVideoStoryRequest(BaseModel):
    username: Annotated[str, Form()]
    photo_path: Annotated[str, Form()]


class PaginationMetadata(BaseModel):
    total: int
    current_page: int
    page_size: int


class PaginatedResponse(BaseModel):
    metadata: PaginationMetadata
    data: List[UserIGOut]
