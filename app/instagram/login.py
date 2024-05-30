from typing import Dict
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from app.crud.user_ig import update_user_session
from app.proxy.utils import is_proxy_usable
from app.logger.utils import logger


def login_instagram(
    username: str, password: str, proxy: str = None, session: Dict = None
):
    logger.info("Try to Logging to Instagram")

    cl = Client()

    if proxy and is_proxy_usable(proxy):
        usability = "usable" if is_proxy_usable(proxy) else "not usable"
        logger.info("Proxy {} is {}".format(proxy, usability))
        cl.set_proxy(proxy)

    login_via_session = False
    login_via_pw = False

    if session:
        logger.info("Trying to login with session...")

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

    if not login_via_session:
        try:
            logger.info(
                "Attempting to login via username and password. username: %s" % username
            )
            if cl.login(username, password):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)
            login_via_pw = False

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

    # Implement update user session here
    update_user_session(username, cl.get_settings())

    logger.info("succesfully save instagram session")

    return cl
