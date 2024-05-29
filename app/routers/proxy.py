from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.proxy.utils import validate_proxies_concurrently

router = APIRouter()


@router.get("/v1/proxies/validate", response_model=dict)
async def validate_proxies(proxy_urls: List[str] = Query(...)):
    try:
        usable_proxies = validate_proxies_concurrently(proxy_urls)
        return {"usable_proxies": usable_proxies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate proxies: {e}")
