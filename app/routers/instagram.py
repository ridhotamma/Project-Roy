from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.instagram.post import post_image_story, post_video_story, post_content
from app.crud.user_ig import get_user, update_user_session
from app.instagram.login import login_instagram
from app.models.user_ig import (
    LoginRequest,
    CreatePostRequest,
    CreateStoryRequest,
    CreateVideoStoryRequest,
)

router = APIRouter()


@router.post("/v1/instagram/test-login", response_model=dict)
async def test_login_instagram(request: LoginRequest):
    try:
        user = get_user(request.username)
        user_session = user.session.model_dump() if user.session else None
        cl = login_instagram(
            request.username,
            request.password,
            user.proxy_url,
            user_session,
        )
        update_user_session(request.username, cl.get_settings())
        user = get_user(request.username)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Login success",
                "data": user.model_dump(),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to login to instagram: {e}",
        )


@router.post("/v1/instagram/image-story", response_model=dict)
async def create_image_story(request: CreateStoryRequest):
    try:
        user = get_user(request.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        cl = login_instagram(user.username, user.password)
        story_result = post_image_story(cl, request.photo_path)
        return {"detail": f"Story posted: {story_result}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to post story: {e}",
        )


@router.post("/v1/instagram/video-story", response_model=dict)
async def create_video_story(request: CreateVideoStoryRequest):
    try:
        user = get_user(request.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        cl = login_instagram(user.username, user.password)
        story_result = post_video_story(cl, request.photo_path)
        return {"detail": f"Story posted: {story_result}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to post story: {e}",
        )


@router.post("/v1/instagram/post-content", response_model=dict)
async def create_post(request: CreatePostRequest):
    try:
        user = get_user(request.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        cl = login_instagram(user.username, user.password)
        content_result = post_content(cl, request.photo_path, request.caption)
        return {"detail": f"Content posted: {content_result}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to post content: {e}",
        )
