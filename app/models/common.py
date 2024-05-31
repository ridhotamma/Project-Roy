from pydantic import BaseModel
from typing import List, TypeVar, Generic

T = TypeVar("T")


class PaginationMetadata(BaseModel):
    total: int
    current_page: int
    page_size: int


class PaginatedResponse(BaseModel, Generic[T]):
    metadata: PaginationMetadata
    data: List[T]
