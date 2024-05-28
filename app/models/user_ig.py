from pydantic import BaseModel, Field
from typing import Optional


class UserIG(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    proxy_url: Optional[str] = Field(None, regex=r'^http://.*|https://.*')

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword",
                "proxy_url": "http://proxy.example.com:8080"
            }
        }
