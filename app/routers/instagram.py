from fastapi import APIRouter, HTTPException
from app.instagram.login import login
from app.instagram.post import post_image_story, post_video_story, post_content
from app.crud.user_ig import get_user

router = APIRouter()


@router.post("/v1/instagram/image-story", response_model=dict)
async def create_image_story(username: str, photo_path: str):
    try:
        user = get_user(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        cl = login(user.username, user.password)
        story_result = post_image_story(cl, photo_path)
        return {"detail": f"Story posted: {story_result}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to post story: {e}")


@router.post("/v1/instagram/video-story", response_model=dict)
async def create_video_story(username: str, photo_path: str):
    try:
        user = get_user(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        cl = login(user.username, user.password)
        story_result = post_video_story(cl, photo_path)
        return {"detail": f"Story posted: {story_result}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to post story: {e}")


@router.post("/v1/instagram/post-content", response_model=dict)
async def create_post(username: str, photo_path: str, caption: str):
    try:
        user = get_user(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        cl = login(user.username, user.password)
        content_result = post_content(cl, photo_path, caption)
        return {"detail": f"Content posted: {content_result}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to post content: {e}")
