import json
from flask import session, abort
from datetime import datetime

from app.core.db import get_db


def get_session():
    """
    Retrieves the user_id for the user accessing the session
    Works as an Authentication system to ensure their session is valid
    """

    username = session.get("user_id")

    if not username:
        abort(401)

    return username


def parse_multi_db_data(data):
    """
    Converts sql.Row to Dict for processing
    Casts Boolean stored as Integers (SQLite3 limitation) as Boolean
    """

    # Generator comprehension to save memory, even though memory usage negligible here
    data = (dict(row) for row in data)

    list_of_data = []

    for row in data:
        if "chargeable" in row:
            row["chargeable"] = bool(row["chargeable"])
        elif "from_tenant" in row:
            row["from_tenant"] = bool(row["from_tenant"])

        list_of_data.append(dict(row))

    return list_of_data


def parse_single_db_data(data):
    return dict(data)


def log_to_db(data):
    con = get_db()
    with con:
        con.execute(
            """INSERT INTO logs (log, date) VALUES (:log, :date)""",
            {"log": json.dumps(data), "date": datetime.now().isoformat()},
        )
