from app.core.utils import (
    get_session,
    parse_multi_db_data,
    log_to_db,
    parse_single_db_data,
)
from app.core.db import get_db
from flask import abort


def single_user_payments():

    username = get_session()

    c = get_db().cursor()
    c.execute("""SELECT * FROM payments WHERE user_id == :user""", {"user": username})
    data = c.fetchall()

    if not data:
        abort(404)

    list_of_payments = parse_multi_db_data(data)

    return list_of_payments


def all_user_payments():

    # Only using to validate user is authenticated
    get_session()

    c = get_db().cursor()
    c.execute("""SELECT * FROM payments""")
    data = c.fetchall()

    if not data:
        abort(404)

    list_of_payments = parse_multi_db_data(data)

    return list_of_payments


def insert_payment(body):

    username = get_session()

    con = get_db()
    with con:
        con.execute(
            """INSERT INTO payments 
        (user_id, paid, date, reason, from_tenant) 
        VALUES 
        (:user_id, :paid, :date, :reason, :from_tenant)""",
            {
                "user_id": username,
                "paid": body["paid"],
                "date": body["date"],
                "reason": body["reason"],
                "from_tenant": body["from_tenant"],
            },
        )

    log_msg = {
        "message": f"Values inserted into payments by {username}",
        "values": [
            username,
            body["paid"],
            body["reason"],
            body["date"],
            body["from_tenant"],
        ],
    }

    log_to_db(log_msg)


def delete_payment(id):
    username = get_session()
    con = get_db()

    with con:
        data = con.execute(
            """SELECT * FROM payments WHERE id == :id""", {"id": id}
        ).fetchone()

        if not data:
            abort(404)

        con.execute("""DELETE FROM payments WHERE id == :id""", {"id": id})

    data = parse_single_db_data(data)

    log_msg = {
        "message": f"Values Deleted from payments by {username}",
        "values": [
            username,
            data["paid"],
            data["reason"],
            data["date"],
            data["from_tenant"],
        ],
    }

    log_to_db(log_msg)


def update_payment(body):

    username = get_session()
    con = get_db()
    with con:
        data = con.execute(
            """SELECT * FROM payments WHERE id == :id""", {"id": body["id"]}
        ).fetchone()

        if not data:
            abort(404)

        con.execute(
            """UPDATE payments
        SET 
        paid = :paid,
        date = :date,
        reason = :reason,
        from_tenant = :from_tenant
        WHERE id == :id""",
            {
                "paid": body["paid"],
                "date": body["date"],
                "reason": body["reason"],
                "from_tenant": body["from_tenant"],
                "id": body["id"],
            },
        )

    data = parse_single_db_data(data)

    log_msg = {
        "message": f"Values updated in payments by {username}",
        "prev_values": [
            username,
            data["paid"],
            data["reason"],
            data["date"],
            data["from_tenant"],
        ],
        "new_values": [
            username,
            body["paid"],
            body["reason"],
            body["date"],
            body["from_tenant"],
        ],
    }

    log_to_db(log_msg)
