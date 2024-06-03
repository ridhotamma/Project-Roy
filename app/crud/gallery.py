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
        gallery_collection.insert_one(gallery.model_dump())
        return gallery
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Gallery already exists")


def get_galleries(skip: int = 0, limit: int = 10) -> List[Gallery]:
    gallery_collection = get_gallery_collection()
    galleries_cursor = gallery_collection.find().skip(skip).limit(limit)
    galleries = [Gallery(**gallery) for gallery in galleries_cursor]
    gallery_total = gallery_collection.count_documents({})
    current_page = skip // limit + 1

    metadata = PaginationMetadata(total=gallery_total, current_page=current_page, page_size=limit)

    return PaginatedResponse(metadata=metadata, data=galleries)


def get_gallery(id: str):
    gallery_collection = get_gallery_collection()
    gallery = gallery_collection.find_one({"id": id})
    if gallery:
        return Gallery(**gallery)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found")


def update_gallery(id: str, gallery: Gallery):
    gallery_collection = get_gallery_collection()
    current_gallery = gallery_collection.find_one({"id": id})
    if not current_gallery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found")

    gallery.update_timestamp()
    updated_fields = {}
    for key, value in gallery.model_dump(exclude_unset=True).items():
        if current_gallery.get(key) != value:
            updated_fields[key] = value

    if not updated_fields:
        return Gallery(**current_gallery)

    updated_fields["updated_at"] = datetime.now(timezone.utc)
    result = gallery_collection.update_one({"id": id}, {"$set": updated_fields})
    if result.matched_count:
        current_gallery.update(updated_fields)
        return Gallery(**current_gallery)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found")


def delete_gallery(id: str):
    gallery_collection = get_gallery_collection()
    result = gallery_collection.delete_one({"id": id})
    if result.deleted_count:
        return {"detail": "Gallery deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found")


def add_image_to_gallery(gallery_id: str, image: GalleryImage):
    gallery_collection = get_gallery_collection()
    gallery = gallery_collection.find_one({"id": gallery_id})
    if gallery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found")
    image.update_timestamp()
    gallery["images"].append(image.model_dump())
    gallery["updated_at"] = datetime.now(timezone.utc)
    result = gallery_collection.update_one(
        {"id": gallery_id}, {"$set": {"images": gallery["images"], "updated_at": gallery["updated_at"]}}
    )
    if result.modified_count:
        return Gallery(**gallery)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to add image to gallery",
    )


def delete_image_from_gallery(gallery_id: str, image_id: str):
    gallery_collection = get_gallery_collection()
    gallery = gallery_collection.find_one({"id": gallery_id})
    if gallery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery not found")

    updated_gallery_images = [image for image in gallery["images"] if image["id"] != image_id]
    if len(updated_gallery_images) == len(gallery["images"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    gallery["images"] = updated_gallery_images
    gallery["updated_at"] = datetime.now(timezone.utc)
    result = gallery_collection.update_one(
        {"id": gallery_id}, {"$set": {"images": gallery["images"], "updated_at": gallery["updated_at"]}}
    )
    if result.modified_count:
        return {"detail": "Image deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update gallery",
        )
