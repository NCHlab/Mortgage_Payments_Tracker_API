from flask import session, abort


def get_session():
    username = session.get("user_id")

    if not username:
        abort(401)

    return username


def parse_db_data(data):
    return [dict(row) for row in data]