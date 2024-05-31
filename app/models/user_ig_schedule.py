from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Union
from app.models.user_ig_post import UserIGPost
from app.models.user_ig_story import UserIGStory
import uuid


class UserIGSchedule(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action_type: str = Field(..., pattern=r"^(post_content|post_story)$")
    username: str = Field(..., min_length=3, max_length=50)
    scheduled_item: Union[UserIGPost, UserIGStory]
    scheduled_time: datetime

    @field_validator("scheduled_item")
    def validate_scheduled_item(cls, value, values):
        if values["action_type"] == "post_content" and not isinstance(
            value, UserIGPost
        ):
            raise ValueError(
                "scheduled_item must be of type UserIGPost for post_content action"
            )
        if values["action_type"] == "post_story" and not isinstance(value, UserIGStory):
            raise ValueError(
                "scheduled_item must be of type UserIGStory for post_story action"
            )
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "action_type": "post_content",
                "username": "johndoe",
                "scheduled_item": {
                    "username": "johndoe",
                    "photo_path": "path/to/photo.jpg",
                    "caption": "This is a caption",
                },
                "scheduled_time": "2024-05-30T10:00:00",
            }
        }
