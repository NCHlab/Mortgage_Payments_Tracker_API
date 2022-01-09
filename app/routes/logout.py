from flask import session

from app.core.session import get_session


def logout_endpoint() -> tuple:

    get_session()
    session.clear()

    return "", 204
