import sqlite3
from flask import g, abort
from typing import Type

from app.core.configs import Config

config = Config()


def get_db() -> Type[sqlite3.Connection]:
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(config.MPT_DATABASE_PATH + "mortgage.db")
        db.row_factory = sqlite3.Row

    return db


def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def get_user_info(username: str) -> Type[sqlite3.Row]:
    c = get_db().cursor()
    c.execute(
        "SELECT username, password, login_attempt, locked FROM users WHERE username == :user",
        {"user": username},
    )

    data = c.fetchone()
    if data is None:
        abort(401)

    return data


def set_user_info(username, attempts, locked):
    con = get_db()

    with con:
        con.execute(
            "UPDATE users SET login_attempt = :login_attempt, locked = :locked WHERE username == :user",
            {"user": username, "login_attempt": attempts, "locked": locked},
        )
