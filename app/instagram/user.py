from typing import List
from instagrapi import Client
from instagrapi.types import UserShort


def get_user_info(cl: Client, username: str) -> str:
    result = cl.user_id_from_username(username)
    return result


def get_user_followers(cl: Client, user_id: str) -> List[UserShort]:
    result = cl.user_followers_gql(user_id)
    return result


def get_user_followings(cl: Client, user_id: str) -> List[UserShort]:
    result = cl.user_following_gql(user_id)
    return result
