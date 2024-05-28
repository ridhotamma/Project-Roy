from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserIGSchedule(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    photo_path: str
    caption: Optional[str]
    scheduled_time: datetime

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "photo_path": "path/to/photo.jpg",
                "caption": "This is a caption",
                "scheduled_time": "2024-05-30T10:00:00"
            }
        }
