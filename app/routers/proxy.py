from fastapi import APIRouter, HTTPException, Query, status, File, UploadFile
from typing import List
from app.proxy.utils import validate_proxies_concurrently

router = APIRouter()


@router.get("/proxies/validate", response_model=dict)
async def validate_proxies(proxy_urls: List[str] = Query(...)):
    try:
        usable_proxies = validate_proxies_concurrently(proxy_urls)
        return {"usable_proxies": usable_proxies}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate proxies: {e}",
        )


@router.post("/proxies/validate_from_file", response_model=dict)
async def validate_proxies_from_file(
    file: UploadFile = File(
        ...,
        description="Upload a .txt file with comma-separated proxy URLs (e.g., http://proxy1:port,http://proxy2:port",
    )
):
    try:
        contents = await file.read()
        proxy_urls = contents.decode("utf-8").split(",")
        proxy_urls = [proxy.strip() for proxy in proxy_urls if proxy.strip()]
        usable_proxies = validate_proxies_concurrently(proxy_urls)
        return {"usable_proxies": usable_proxies}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate proxies: {e}",
        )
