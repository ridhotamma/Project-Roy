from fastapi import APIRouter, HTTPException, Depends
from app.instagram.login import login
from app.instagram.post import post_story, post_content
from app.models.user_ig import UserIG
from app.crud.user_ig import get_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

# OAuth2 scheme for user authentication (modify as needed for your authentication method)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(username: str):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/v1/instagram/story", response_model=dict)
async def create_story(username: str, photo_path: str):
    try:
        user = get_user(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        cl = login(user.username, user.password)
        story_result = post_story(cl, photo_path)
        return {"detail": f"Story posted: {story_result}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to post story: {e}")

@router.post("/v1/instagram/post", response_model=dict)
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
