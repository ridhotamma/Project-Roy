from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone


class GalleryImage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    image_url: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc()))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc()))

    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc())


class Gallery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    images: List[GalleryImage] = []
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc()))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc()))

    def update_timestamp(self):
        self.updated_at = datetime.now()
