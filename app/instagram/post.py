def post_story(cl, photo_path):
    result = cl.photo_upload_to_story(photo_path)
    return result


def post_content(cl, photo_path, caption):
    result = cl.photo_upload(photo_path, caption)
    return result
