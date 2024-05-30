from typing import List
from pydantic import BaseModel, Field


class UserIGPost(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    photo_path: str
    caption: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "photo_path": "path/to/photo.jpg",
                "caption": "This is a caption",
            }
        }


class PaginationMetadata(BaseModel):
    total: int
    current_page: int
    page_size: int


class PaginatedResponse(BaseModel):
    metadata: PaginationMetadata
    data: List[UserIGPost]
