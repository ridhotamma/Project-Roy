from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.instagram.post import post_image_story, post_video_story, post_content
from app.crud.user_ig import get_user, update_user_session
from app.instagram.login import login_instagram
from app.instagram.utils import (
    download_image,
    delete_image,
    generate_save_path,
    generate_preview_url,
)
from app.models.user_ig import (
    LoginRequest,
    CreatePostRequest,
    CreateStoryRequest,
    CreateVideoStoryRequest,
)

router = APIRouter()


@router.post("/instagram/test-login", response_model=dict)
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


@router.post("/instagram/image-story", response_model=dict)
async def create_image_story(request: CreateStoryRequest):
    try:
        user = get_user(request.username)
        user_session = user.session.model_dump() if user.session else None
        cl = login_instagram(
            request.username,
            request.password,
            user.proxy_url,
            user_session,
        )

        cl = login_instagram(user.username, user.password, user.proxy_url, user_session)
        story_result = post_image_story(cl, request.photo_path)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Upload story success",
                "data": story_result,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to post story: {e}",
        )


@router.post("/instagram/video-story", response_model=dict)
async def create_video_story(request: CreateVideoStoryRequest):
    try:
        user = get_user(request.username)
        user_session = user.session.model_dump() if user.session else None
        cl = login_instagram(
            request.username,
            request.password,
            user.proxy_url,
            user_session,
        )

        cl = login_instagram(user.username, user.password, user.proxy_url, user_session)
        story_result = post_video_story(cl, request.photo_path)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Upload story success",
                "data": story_result,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to post story: {e}",
        )


@router.post("/instagram/post-content", response_model=dict)
async def create_post(request: CreatePostRequest):
    save_path = generate_save_path()

    try:
        user = get_user(request.username)
        user_session = user.session.model_dump() if user.session else None
        cl = login_instagram(
            user.username,
            user.password,
            user.proxy_url,
            user_session,
        )

        download_image(request.photo_path, save_path)
        content_result = post_content(cl, save_path, request.caption)
        preview_url = generate_preview_url(content_result)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Upload post success",
                "detail": {"preview_url": preview_url},
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to post content: {e}",
        )
    finally:
        delete_image(save_path)
