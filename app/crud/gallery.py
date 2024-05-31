from typing import List
from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException, status
from app.database import get_gallery_collection
from app.models.gallery import Gallery, GalleryImage
from app.models.common import PaginationMetadata, PaginatedResponse


def create_gallery(gallery: Gallery):
    gallery_collection = get_gallery_collection()
    gallery.update_timestamp()
    try:
        gallery_collection.insert_one(gallery.dict())
        return gallery
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Gallery already exists"
        )


def get_galleries(skip: int = 0, limit: int = 10) -> List[Gallery]:
    gallery_collection = get_gallery_collection()
    galleries_cursor = gallery_collection.find().skip(skip).limit(limit)
    galleries = [Gallery(**gallery) for gallery in galleries_cursor]
    gallery_total = gallery_collection.count_documents({})
    current_page = skip // limit + 1

    metadata = PaginationMetadata(
        total=gallery_total, current_page=current_page, page_size=limit
    )

    return PaginatedResponse(metadata=metadata, data=galleries)


def get_gallery(id: str):
    gallery_collection = get_gallery_collection()
    gallery = gallery_collection.find_one({"id": id})
    if gallery:
        return Gallery(**gallery)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found"
    )


def update_gallery(id: str, gallery: Gallery):
    gallery_collection = get_gallery_collection()
    gallery.update_timestamp()
    result = gallery_collection.update_one({"id": id}, {"$set": gallery.dict()})
    if result.matched_count:
        return gallery
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found"
    )


def delete_gallery(id: str):
    gallery_collection = get_gallery_collection()
    result = gallery_collection.delete_one({"id": id})
    if result.deleted_count:
        return {"detail": "Gallery deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found"
    )


def add_image_to_gallery(gallery_id: str, image: GalleryImage):
    gallery_collection = get_gallery_collection()
    gallery = gallery_collection.find_one({"id": gallery_id})
    if gallery is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found"
        )
    image.update_timestamp()
    gallery["images"].append(image.model_dump())
    gallery["updated_at"] = datetime.now(timezone.utc())
    result = gallery_collection.update_one({"id": gallery_id}, {"$set": gallery})
    if result.modified_count:
        return Gallery(**gallery)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to add image to gallery",
    )
