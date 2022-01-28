import secrets

from app.core.db import get_user_info, set_user_info

from flask import abort


def validate_basic_auth(username: str, password: str) -> dict:
    user_info = None

    db_user, db_pass, attempts, locked = get_user_info(username)

    # secrets.compare_digest secures against timing attacks
    correct_username = secrets.compare_digest(db_user, username)
    correct_password = secrets.compare_digest(db_pass, password)

    if correct_username and correct_password:
        if bool(locked):
            abort(423)

        elif attempts != 0:
            # Set attempts to 0 and locked to 0
            set_user_info(db_user, 0, 0)

        user_info = {"sub": username, "scope": ""}
    else:
        # Arriving here means they have used a username that exists, but wrong password
        if bool(locked) or attempts >= 4:
            abort(423)
        else:
            attempts += 1
            if attempts > 3:
                set_user_info(db_user, 4, 1)
                abort(423)
            else:
                set_user_info(db_user, attempts, 0)

    return user_info
