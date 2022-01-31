import connexion
import base64
from datetime import datetime

from app.core.db import get_db
from app.core.db_log import log_to_db
from app.service.common import unauth_demo_login_details


def parse_login() -> str:
    auth = connexion.request.headers["Authorization"]
    username, _ = base64.b64decode(auth[6:]).decode("utf-8").split(":")

    return username


def set_last_login_timestamp(username: str) -> None:
    date_timestamp = datetime.now()

    con = get_db()
    with con:
        con.execute(
            """UPDATE users SET last_login = :date_timestamp WHERE username == :user""",
            {"date_timestamp": date_timestamp.isoformat(), "user": username},
        )

    data = {
        "message": f"{username} logged in",
        "user_id": username,
        "date_timestamp": date_timestamp.isoformat(),
    }

    log_to_db(data, None, "LOGIN")


def retrieve_user_details(username: str) -> dict:

    data = unauth_demo_login_details(username)

    return data


def save_random_password(username: str, password: str) -> None:

    con = get_db()
    with con:
        con.execute(
            f"""UPDATE users SET password = :password WHERE username == :username""",
            {"password": password, "username": username},
        )
