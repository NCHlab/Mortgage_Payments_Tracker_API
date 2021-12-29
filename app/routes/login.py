from flask import session

from app.service.login_service import parse_login, set_last_login_timestamp
from app.core.utils import get_session


def login_endpoint():
    """
    Connexion handles authentication, so if a request reaches here, they have been authenticated via DB
    Sets the username into the session and returns the user_id to user.
    """

    username = parse_login()

    response = {"user_id": username}
    session["user_id"] = username

    set_last_login_timestamp(username)

    return response


def get_login():
    get_session()
