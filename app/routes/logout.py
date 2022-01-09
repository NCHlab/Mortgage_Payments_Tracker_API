from flask import session

from app.core.session import get_session


def logout_endpoint():

    get_session()
    session.clear()

    return "", 204
