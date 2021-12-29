from flask import g, abort
import sqlite3


from app.core.configs import Config

config = Config()


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(config.MPT_DATABASE_PATH + "mortgage.db")
        db.row_factory = sqlite3.Row
    return db


def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def get_user_info(username):
    c = get_db().cursor()
    c.execute(
        "SELECT username, password FROM users WHERE username == :user",
        {"user": username},
    )

    data = c.fetchone()
    if data is None:
        abort(401)

    return data
