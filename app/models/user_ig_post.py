from pydantic import BaseModel, Field
import uuid


class UserIGPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
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
