import secrets

from app.core.db import get_user_info


def validate_basic_auth(username: str, password: str) -> dict:
    user_info = None

    db_user, db_pass = get_user_info(username)

    # secrets.compare_digest secures against timing attacks
    correct_username = secrets.compare_digest(db_user, username)
    correct_password = secrets.compare_digest(db_pass, password)

    if correct_username and correct_password:
        user_info = {"sub": username, "scope": ""}

    return user_info
