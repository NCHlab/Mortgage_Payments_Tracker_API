import connexion
import base64
from datetime import datetime

from app.core.db import get_db


def parse_login():
    auth = connexion.request.headers["Authorization"]
    username, _ = base64.b64decode(auth[6:]).decode("utf-8").split(":")

    return username


def set_last_login_timestamp(username):
    date_timestamp = datetime.now()

    con = get_db()
    with con:
        con.execute(
            """UPDATE users SET last_login = :date_timestamp WHERE username == :user""",
            {"date_timestamp": date_timestamp.isoformat(), "user": username},
        )
