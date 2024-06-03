from typing import List
from instagrapi import Client
from instagrapi.types import UserShort, User
from app.logger.utils import logger


def get_user_id(cl: Client, username: str) -> str:
    logger.info("[app.instagram.user]: Getting user id by username")
    result = cl.user_id_from_username(username)
    return result


def get_user_info(cl: Client, user_id: str) -> User:
    logger.info("[app.instagram.user]: Getting user info by user id")
    result = cl.user_info_v1(user_id)
    return result


def get_user_followers(cl: Client, user_id: str) -> List[UserShort]:
    logger.info("[app.instagram.user]: Getting user followers by user id")
    result = cl.user_followers_gql(user_id)
    return result


def get_user_followings(cl: Client, user_id: str) -> List[UserShort]:
    logger.info("[app.instagram.user]: Getting user followings by user id")
    result = cl.user_following_gql(user_id)
    return result
