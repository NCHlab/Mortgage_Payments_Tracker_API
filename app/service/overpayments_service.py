from app.core.utils import (
    get_session,
    parse_multi_db_data,
    log_to_db,
    parse_single_db_data,
)
from app.core.db import get_db
from flask import abort


def single_user_overpayments():

    username = get_session()

    c = get_db().cursor()
    c.execute(
        """SELECT * FROM overpayments WHERE user_id == :user""", {"user": username}
    )
    data = c.fetchall()

    if not data:
        abort(404)

    list_of_payments = parse_multi_db_data(data)

    return list_of_payments


def all_user_overpayments():

    # Only using to validate user is authenticated
    get_session()

    c = get_db().cursor()
    c.execute("""SELECT * FROM overpayments""")
    data = c.fetchall()

    if not data:
        abort(404)

    list_of_payments = parse_multi_db_data(data)

    return list_of_payments


def insert_overpayment(body):

    username = get_session()

    con = get_db()
    with con:
        con.execute(
            """INSERT INTO overpayments 
        (user_id, paid, date, reason) 
        VALUES 
        (:user_id, :paid, :date, :reason)""",
            {
                "user_id": username,
                "paid": body["paid"],
                "date": body["date"],
                "reason": body["reason"],
            },
        )

    log_msg = {
        "message": f"Values inserted into overpayments by {username}",
        "values": [
            username,
            body["paid"],
            body["reason"],
            body["date"],
        ],
    }

    log_to_db(log_msg)


def delete_overpayment(id):
    username = get_session()
    con = get_db()

    with con:
        data = con.execute(
            """SELECT * FROM overpayments WHERE id == :id""", {"id": id}
        ).fetchone()

        if not data:
            abort(404)

        con.execute("""DELETE FROM overpayments WHERE id == :id""", {"id": id})

    data = parse_single_db_data(data)

    log_msg = {
        "message": f"Values Deleted from overpayments by {username}",
        "values": [
            username,
            data["paid"],
            data["reason"],
            data["date"],
        ],
    }

    log_to_db(log_msg)


def update_overpayment(body):

    username = get_session()
    con = get_db()
    with con:
        data = con.execute(
            """SELECT * FROM overpayments WHERE id == :id""", {"id": body["id"]}
        ).fetchone()

        if not data:
            abort(404)

        con.execute(
            """UPDATE overpayments
        SET 
        paid = :paid,
        date = :date,
        reason = :reason
        WHERE id == :id""",
            {
                "paid": body["paid"],
                "date": body["date"],
                "reason": body["reason"],
                "id": body["id"],
            },
        )

    data = parse_single_db_data(data)

    log_msg = {
        "message": f"Values updated in overpayments by {username}",
        "prev_values": [
            username,
            data["paid"],
            data["reason"],
            data["date"],
        ],
        "new_values": [
            username,
            body["paid"],
            body["reason"],
            body["date"],
        ],
    }

    log_to_db(log_msg)
