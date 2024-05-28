from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging

logger = logging.getLogger()


def login(username, password):
    cl = Client()
    try:
        cl.load_settings("session.json")
    except FileNotFoundError:
        logger.info("No existing session found. Proceeding with login.")

    login_via_session = False
    login_via_pw = False

    if cl.settings:
        try:
            cl.set_settings(cl.settings)
            cl.login(username, password)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info(
                    "Session is invalid, need to login via username and password")

                old_settings = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_settings["uuids"])

                cl.login(username, password)
            login_via_session = True
        except Exception as e:
            logger.info(
                "Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info(
                "Attempting to login via username and password. username: %s" % username)
            if cl.login(username, password):
                login_via_pw = True
        except Exception as e:
            logger.info(
                "Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

    # Save session to file
    cl.dump_settings("session.json")

    return cl
