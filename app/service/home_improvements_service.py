from app.core.utils import (
    get_session,
    parse_multi_db_data,
    log_to_db,
    parse_single_db_data,
)
from app.core.db import get_db
from flask import abort


def single_user_home_improvements():

    username = get_session()

    c = get_db().cursor()
    c.execute(
        """SELECT * FROM home_improvements WHERE user_id == :user""", {"user": username}
    )
    data = c.fetchall()

    if not data:
        return []

    list_of_payments = parse_multi_db_data(data)

    return list_of_payments


def all_user_home_improvements():

    # Only using to validate user is authenticated
    get_session()

    c = get_db().cursor()
    c.execute("""SELECT * FROM home_improvements""")
    data = c.fetchall()

    if not data:
        return []

    list_of_payments = parse_multi_db_data(data)

    return list_of_payments


def insert_home_improvements(body):

    username = get_session()

    con = get_db()
    with con:
        con.execute(
            """INSERT INTO home_improvements 
        (user_id, paid, chargeable, date, reason) 
        VALUES 
        (:user_id, :paid, :chargeable, :date, :reason)""",
            {
                "user_id": username,
                "paid": body["paid"],
                "chargeable": body["chargeable"],
                "date": body["date"],
                "reason": body["reason"],
            },
        )

    log_msg = {
        "message": f"Values inserted into home_improvements by {username}",
        "values": [
            username,
            body["paid"],
            body["reason"],
            body["date"],
            body["chargeable"],
        ],
    }

    log_to_db(log_msg)


def delete_home_improvements(id):
    username = get_session()
    con = get_db()

    with con:
        data = con.execute(
            """SELECT * FROM home_improvements WHERE id == :id""", {"id": id}
        ).fetchone()

        if not data:
            abort(404)

        con.execute("""DELETE FROM home_improvements WHERE id == :id""", {"id": id})

    data = parse_single_db_data(data)

    log_msg = {
        "message": f"Values Deleted from home_improvements by {username}",
        "values": [
            username,
            data["paid"],
            data["reason"],
            data["date"],
            data["chargeable"],
        ],
    }

    log_to_db(log_msg)


def update_home_improvements(body):

    username = get_session()
    con = get_db()
    with con:
        data = con.execute(
            """SELECT * FROM home_improvements WHERE id == :id""", {"id": body["id"]}
        ).fetchone()

        if not data:
            abort(404)

        con.execute(
            """UPDATE home_improvements
        SET 
        paid = :paid,
        date = :date,
        reason = :reason,
        chargeable = :chargeable
        WHERE id == :id""",
            {
                "paid": body["paid"],
                "date": body["date"],
                "reason": body["reason"],
                "chargeable": body["chargeable"],
                "id": body["id"],
            },
        )

    data = parse_single_db_data(data)

    log_msg = {
        "message": f"Values updated in home_improvements by {username}",
        "prev_values": [
            username,
            data["paid"],
            data["reason"],
            data["date"],
            data["chargeable"],
        ],
        "new_values": [
            username,
            body["paid"],
            body["reason"],
            body["date"],
            body["chargeable"],
        ],
    }

    log_to_db(log_msg)
