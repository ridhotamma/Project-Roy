from pydantic import BaseModel, Field, model_validator
from datetime import datetime, timezone
from typing import Union, Optional, Any
from typing_extensions import Self
from app.models.user_ig_post import UserIGPost
from app.models.user_ig_story import UserIGStory

import uuid


class UserIGSchedule(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action_type: str = Field(..., pattern=r"^(post_content|post_story)$")
    status_type: str = Field(..., pattern=r"^(success|failed|expired|unprocessed)$")
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_item: Union[UserIGPost, UserIGStory]
    scheduled_time: datetime
    error: Any = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def validate_scheduled_item(self) -> Self:
        action_type = self.action_type
        scheduled_item = self.scheduled_item

        if action_type == "post_content" and not isinstance(scheduled_item, UserIGPost):
            raise ValueError("scheduled_item must be of type UserIGPost for post_content action")
        if action_type == "post_story" and not isinstance(scheduled_item, UserIGStory):
            raise ValueError("scheduled_item must be of type UserIGStory for post_story action")
        return self

    @property
    def formatted_schedule_time(self) -> str:
        format: str = "%A, %d %B %Y %H:%M:%S"
        return self.scheduled_time.strftime(format)

    class Config:
        json_schema_extra = {
            "example": {
                "action_type": "post_content",
                "title": "lorem ipsum",
                "description": "lorem ipsum",
                "scheduled_item": {
                    "username": "johndoe",
                    "photo_path": "https://asdf.cloudfront.net/example.jpg",
                    "caption": "This is a caption",
                },
                "scheduled_time": "2024-05-30T10:00:00",
            }
        }
