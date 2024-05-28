from pydantic import BaseModel, Field


class UserIGStory(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    photo_path: str

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "photo_path": "path/to/photo.jpg"
            }
        }
