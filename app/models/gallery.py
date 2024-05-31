from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime


class GalleryImage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    image_url: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()


class Gallery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    images: List[GalleryImage] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
