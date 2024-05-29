from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
from app.crud.user_ig import update_user_session, get_user
from app.proxy.utils import is_proxy_usable

logger = logging.getLogger()


def login(username, password):
    cl = Client()

    user = get_user(username)

    if not user:
        raise ValueError(f"User {username} not found")

    if user.proxy_url and is_proxy_usable(user.proxy_url):
        cl.set_proxy(user.proxy_url)

    if user.session:
        session_data = user.session
        try:
            cl.set_settings(session_data)
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

    return cl
