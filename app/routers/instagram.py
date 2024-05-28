from fastapi import APIRouter, HTTPException
from app.instagram.login import login
from app.instagram.post import post_story, post_content

router = APIRouter()

USERNAME = ''
PASSWORD = ''

# Global client variable
cl = None

@router.on_event("startup")
async def startup_event():
    global cl
    try:
        cl = login(USERNAME, PASSWORD)
        print("Logged in successfully")
    except Exception as e:
        print(f"Login failed: {e}")

@router.post("/v1/instagram/story", response_model=dict)
async def create_story(photo_path: str):
    try:
        story_result = post_story(cl, photo_path)
        return {"detail": f"Story posted: {story_result}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to post story: {e}")

@router.post("/v1/instagram/post", response_model=dict)
async def create_post(photo_path: str, caption: str):
    try:
        content_result = post_content(cl, photo_path, caption)
        return {"detail": f"Content posted: {content_result}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to post content: {e}")
