from instagrapi.story import StoryBuilder
from instagrapi import Client
from instagrapi.types import Story, Media


def post_image_story(cl: Client, photo_path: str) -> Story:
    result = cl.photo_upload_to_story(photo_path)
    return result


def post_video_story(cl: Client, video_path: str) -> Story:
    buildout = StoryBuilder(path=video_path,).video(
        15
    )  # seconds

    result = cl.video_upload_to_story(
        buildout.path,
    )
    return result


def post_content(cl: Client, photo_path: str, caption: str) -> Media:
    result = cl.photo_upload(photo_path, caption)
    return result
