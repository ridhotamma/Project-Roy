from fastapi import APIRouter, Query
from app.models.gallery import Gallery, GalleryImage
from app.models.common import PaginatedResponse
from app.crud import gallery as crud_gallery

router = APIRouter()


@router.post("/galleries", response_model=Gallery)
async def create_gallery(gallery: Gallery):
    return crud_gallery.create_gallery(gallery)


@router.get("/galleries", response_model=PaginatedResponse)
async def get_galleries(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    return crud_gallery.get_galleries(skip, limit)


@router.get("/galleries/{id}", response_model=Gallery)
async def get_gallery(id: str):
    return crud_gallery.get_gallery(id)


@router.put("/galleries/{id}", response_model=Gallery)
async def update_gallery(id: str, gallery: Gallery):
    return crud_gallery.update_gallery(id, gallery)


@router.delete("/galleries/{id}", response_model=dict)
async def delete_gallery(id: str):
    return crud_gallery.delete_gallery(id)


@router.post("/galleries/{gallery_id}/images", response_model=Gallery)
async def add_image_to_gallery(gallery_id: str, image: GalleryImage):
    return crud_gallery.add_image_to_gallery(gallery_id, image)


@router.put("/galleries/{gallery_id}/images/{image_id}", response_model=dict)
async def remove_image_from_gallery(gallery_id: str, image_id: str):
    return crud_gallery.delete_image_from_gallery(gallery_id, image_id)
