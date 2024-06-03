from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.crud.user_ig import get_user, update_user
from app.instagram.post import post_image_story, post_video_story, post_content
from app.instagram.login import login_instagram
from app.instagram.user import get_user_followers, get_user_followings, get_user_info
from app.instagram.utils import (
    download_image,
    delete_image,
    generate_save_path,
    generate_preview_url,
    update_user_session,
)
from app.models.user_ig import (
    LoginRequest,
    CreatePostRequest,
    CreateStoryRequest,
    CreateVideoStoryRequest,
    GetUserRequest,
    SyncUserRequest,
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
                "data": cl.get_settings(),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to login to instagram: {e}",
        )


@router.post("/instagram/image-story", response_model=dict)
async def create_image_story(request: CreateStoryRequest):
    save_path = generate_save_path()

    try:
        user = get_user(request.username)
        user_session = user.session.model_dump() if user.session else None
        cl = login_instagram(
            request.username,
            request.password,
            user.proxy_url,
            user_session,
        )
        download_image(request.photo_path, save_path)
        story_result = str(post_image_story(cl, save_path))
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
    finally:
        delete_image(save_path)


@router.post("/instagram/video-story", response_model=dict)
async def create_video_story(request: CreateVideoStoryRequest):
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
        story_result = str(post_video_story(cl, save_path))

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Upload story success",
                "detail": story_result,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to post story: {e}",
        )
    finally:
        delete_image(save_path)


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


@router.post("/instagram/followers", response_model=dict)
async def get_user_followers_by_username(request: GetUserRequest):
    try:
        user_logged_in = get_user(request.username_logged_in)
        user_session = user_logged_in.session.model_dump() if user_logged_in.session else None

        cl = login_instagram(
            user_logged_in.username,
            user_logged_in.password,
            user_logged_in.proxy_url,
            user_session,
        )

        followers = get_user_followers(cl, request.user_id_target)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Upload post success",
                "detail": {"followers": list(followers)},
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user followers: {e}",
        )


@router.post("/instagram/followings", response_model=dict)
async def get_user_followings_by_username(request: GetUserRequest):
    try:
        user_logged_in = get_user(request.username_logged_in)
        user_session = user_logged_in.session.model_dump() if user_logged_in.session else None

        cl = login_instagram(
            user_logged_in.username,
            user_logged_in.password,
            user_logged_in.proxy_url,
            user_session,
        )

        followings = get_user_followings(cl, request.user_id_target)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Upload post success",
                "detail": {"followings": list(followings)},
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user folowings: {e}",
        )


@router.post("/instagram/info", response_model=dict)
async def get_user_info_by_username(request: GetUserRequest):
    try:
        user_logged_in = get_user(request.username_logged_in)
        user_session = user_logged_in.session.model_dump() if user_logged_in.session else None

        cl = login_instagram(
            user_logged_in.username,
            user_logged_in.password,
            user_logged_in.proxy_url,
            user_session,
        )

        user_info = get_user_info(cl, request.user_id_target)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Upload post success",
                "detail": {"info": str(user_info)},
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user info: {e}",
        )


@router.post("/instagram/sync", response_model=dict)
async def sync_instagram_user_data(request: SyncUserRequest):
    try:
        user_logged_in = get_user(request.username)
        user_session = user_logged_in.session.model_dump() if user_logged_in.session else None

        cl = login_instagram(
            user_logged_in.username,
            user_logged_in.password,
            user_logged_in.proxy_url,
            user_session,
        )

        ig_user_id = cl.user_id
        user_logged_in.user_id = str(ig_user_id)

        update_user(username=request.username, user=user_logged_in)
        ig_user_info = get_user_info(cl, ig_user_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "message": "Upload post success",
                "detail": {"info": str(ig_user_info)},
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user info: {e}",
        )
