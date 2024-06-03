import requests
import os
import uuid
from datetime import datetime, timezone
from fastapi.exceptions import HTTPException
from fastapi import status
from pymongo import ReturnDocument
from app.logger.utils import logger
from app.database import get_ig_user_collection


def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        logger.info(f"[Download Image] Image downloaded to {save_path}")
    else:
        raise Exception(f"[Download Image] Failed to download image. Status code: {response.status_code}")


def delete_image(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"[Download Image] Image deleted: {file_path}")
    else:
        logger.info(f"[Download Image] File does not exist: {file_path}")


def generate_save_path():
    file_name = str(uuid.uuid4())
    tmp_dir = "tmp/"
    os.makedirs(tmp_dir, exist_ok=True)
    image_path = os.path.join(tmp_dir, f"{file_name}.jpg")

    return image_path


def generate_preview_url(data):
    data_string = str(data)
    code_start = data_string.find("code='") + 6
    code_end = data_string.find("'", code_start)
    code = data_string[code_start:code_end]
    preview_url = f"https://www.instagram.com/p/{code}/"

    return preview_url


def update_user_session(username: str, session_data: dict):
    user_collection = get_ig_user_collection()
    session = {
        "uuids": session_data.get("uuids", {}),
        "cookies": session_data.get("cookies", {}),
        "last_login": session_data.get("last_login", datetime.now(timezone.utc).timestamp()),
        "device_settings": session_data.get("device_settings", {}),
        "user_agent": session_data.get("user_agent", ""),
    }
    update_data = {"session": session, "updated_at": datetime.now(timezone.utc)}

    updated_user = user_collection.find_one_and_update(
        {"username": username},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found.",
        )
    logger.info(f"[{username}] Session updated")
    return updated_user
