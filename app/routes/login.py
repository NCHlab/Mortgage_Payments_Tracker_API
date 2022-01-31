from flask import session
from random import randint
import logging

from app.service.login_service import (
    parse_login,
    set_last_login_timestamp,
    retrieve_user_details,
)
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


def demo_login_endpoint() -> dict:

    list_of_users = ["demo1", "demo2", "demo3", "demo4"]
    counter = randint(0, 3)

    username = list_of_users[counter]
    response = retrieve_user_details(username)

    return response
