from app.models.user_ig_post import UserIGPost
from app.models.user_ig_story import UserIGStory
from app.crud.user_ig import get_user
from app.instagram.login import login_instagram
from app.instagram.post import post_image_story
from app.instagram.utils import download_image, generate_save_path, delete_image
from app.logger.utils import logger


def post_content_to_instagram(post: UserIGPost):
    save_path = generate_save_path()
    try:
        user = get_user(post.username)
        user_session = user.session.model_dump() if user.session else None

        cl = login_instagram(
            user.username,
            user.password,
            user.proxy_url,
            user_session,
        )
        download_image(post.photo_path, save_path)
        post_image_story(cl, save_path)
    except Exception as e:
        logger.error(f"Failed to post content to Instagram for {post.username}: {str(e)}", exc_info=True)
        raise
    finally:
        delete_image(save_path)


def post_story_to_instagram(story: UserIGStory):
    save_path = generate_save_path()
    try:
        user = get_user(story.username)
        user_session = user.session.model_dump() if user.session else None

        cl = login_instagram(
            user.username,
            user.password,
            user.proxy_url,
            user_session,
        )
        download_image(story.photo_path, save_path)
        post_image_story(cl, save_path)
    except Exception as e:
        logger.error(f"Failed to post story to Instagram for {story.username}: {str(e)}", exc_info=True)
        raise
    finally:
        delete_image(save_path)
