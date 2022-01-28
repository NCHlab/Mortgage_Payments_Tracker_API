from flask import session
import logging

from app.service.login_service import parse_login, set_last_login_timestamp
from app.core.session import get_session

logger = logging.getLogger(__name__)


def login_endpoint() -> dict:
    """
    Connexion handles authentication, so if a request reaches here, they have been authenticated via DB
    Sets the username into the session and returns the user_id to user.
    """

    username = parse_login()

    response = {"user_id": username}
    session["user_id"] = username

    set_last_login_timestamp(username)

    logger.info(f"{username} Logged in")

    return response


def get_login() -> dict:
    username = get_session()

    return {"message": f"Logged in as {username}"}
