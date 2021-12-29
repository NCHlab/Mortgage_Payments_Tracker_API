from flask import session, abort
from datetime import datetime
from app.core.db import get_db
import json


def get_session():
    username = session.get("user_id")

    if not username:
        abort(401)

    return username


def parse_multi_db_data(data):
    return [dict(row) for row in data]


def parse_single_db_data(data):
    return dict(data)


def log_to_db(data):
    con = get_db()
    with con:
        con.execute(
            """INSERT INTO logs (log, date) VALUES (:log, :date)""",
            {"log": json.dumps(data), "date": datetime.now().isoformat()},
        )
