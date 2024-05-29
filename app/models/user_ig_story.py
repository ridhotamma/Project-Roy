from pydantic import BaseModel, Field

class UserIGStory(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    photo_path: str
    caption: str
    caption_pos_x: int = Field(default=0)
    caption_pos_y: int = Field(default=0)

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "photo_path": "path/to/photo.jpg",
                "caption_pos_x": 10,
                "caption_pos_y": 20,
            }
        }
