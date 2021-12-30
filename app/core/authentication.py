from app.core.db import get_user_info


def validate_basic_auth(username, password):

    db_user, db_pass = get_user_info(username)
    user_info = None

    if username == db_user and password == db_pass:
        user_info = {"sub": username, "scope": ""}

    return user_info
