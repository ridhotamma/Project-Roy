from typing import List
from pydantic import BaseModel, Field
import uuid


class UserIGStory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str = Field(..., min_length=3, max_length=50)
    photo_path: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "photo_path": "path/to/photo.jpg",
            }
        }


class PaginationMetadata(BaseModel):
    total: int
    current_page: int
    page_size: int


class PaginatedResponse(BaseModel):
    metadata: PaginationMetadata
    data: List[UserIGStory]
