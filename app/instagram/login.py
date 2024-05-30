from typing import Dict
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from app.crud.user_ig import update_user_session
from app.proxy.utils import is_proxy_usable

import logging

logger = logging.getLogger()


def login_instagram(
    username: str, password: str, proxy: str = None, session: Dict = None
):
    print("Trying to login instagram...")

    cl = Client()

    if proxy and is_proxy_usable(proxy):
        cl.set_proxy(proxy)

    if session:
        try:
            cl.set_settings(session)
            cl.login(username, password)

            # Check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info(
                    "Session is invalid, need to login via username and password"
                )

                old_settings = cl.get_settings()

                # Use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_settings["uuids"])

                cl.login(username, password)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)
            login_via_session = False
    else:
        login_via_session = False

    if not login_via_session:
        try:
            print(
                "Attempting to login via username and password. username: %s" % username
            )
            if cl.login(username, password):
                login_via_pw = True
        except Exception as e:
            print("Couldn't login user using username and password: %s" % e)
            login_via_pw = False

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

    # Implement update user session here
    update_user_session(username, cl.get_settings())

    return cl
