from flask import abort

from app.core.utils import (
    get_session,
    log_to_db,
    parse_single_db_data,
)
from app.core.db import get_db
from app.service.common import (
    user_data_from_table,
    all_user_data_from_table,
    insert_to_table,
)


def single_user_home_improvements():
    return user_data_from_table("home_improvements")


def all_user_home_improvements():
    return all_user_data_from_table("home_improvements")


def insert_home_improvements(body):

    username = get_session()

    table_name = "home_improvements"
    col_names = "user_id, paid, chargeable, date, reason"
    placeholder = ":user_id, :paid, :chargeable, :date, :reason"
    values = {
        "user_id": username,
        "paid": body["paid"],
        "chargeable": body["chargeable"],
        "date": body["date"],
        "reason": body["reason"],
    }
    log_list = [
        username,
        body["paid"],
        body["reason"],
        body["date"],
        body["chargeable"],
    ]

    insert_to_table(table_name, col_names, placeholder, values, log_list)
    return

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
