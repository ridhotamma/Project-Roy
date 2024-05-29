from instagrapi.story import StoryBuilder


def post_image_story(cl, photo_path):
    result = cl.photo_upload_to_story(photo_path)
    return result


def post_video_story(cl, video_path):
    buildout = StoryBuilder(path=video_path,).video(
        15
    )  # seconds

    result = cl.video_upload_to_story(
        buildout.path,
    )
    return result


def post_content(cl, photo_path, caption):
    result = cl.photo_upload(photo_path, caption)
    return result
