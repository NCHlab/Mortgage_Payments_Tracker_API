from app.core.utils import (
    get_session,
    log_to_db,
    parse_single_db_data,
    parse_multi_db_data,
)
from app.core.db import get_db
from flask import abort


def get_from_table(table_name):

    username = get_session()

    c = get_db().cursor()
    c.execute(
        f"""SELECT * FROM {table_name} WHERE user_id == :user""", {"user": username}
    )
    data = c.fetchall()

    if not data:
        return []

    list_of_payments = parse_multi_db_data(data)

    return list_of_payments


def get_all_from_table(table_name):

    # Using to validate user is authenticated
    get_session()

    c = get_db().cursor()
    c.execute(f"""SELECT * FROM {table_name}""")
    data = c.fetchall()

    if not data:
        return []

    list_of_payments = parse_multi_db_data(data)

    return list_of_payments


def insert_to_table(table_name, col_names, placeholder, values, log_list):
    username = get_session()

    con = get_db()
    with con:
        con.execute(
            f"""INSERT INTO {table_name} ({col_names}) VALUES ({placeholder})""", values
        )

    log_msg = {
        "message": f"Values inserted into {table_name} by {username}",
        "values": log_list,
    }

    log_to_db(log_msg)


def delete_from_table(_id, table_name):
    username = get_session()
    con = get_db()

    with con:
        data = con.execute(
            f"""SELECT * FROM {table_name} WHERE id == :id""", {"id": _id}
        ).fetchone()

        if not data:
            abort(404)

        con.execute(f"""DELETE FROM {table_name} WHERE id == :id""", {"id": _id})

    data = parse_single_db_data(data)

    log_list = list(data.items())

    log_msg = {
        "message": f"Values deleted from {table_name} by {username}",
        "values": log_list,
    }

    log_to_db(log_msg)


def update_table(_id, table_name, col_names_and_placeholder, values):

    username = get_session()
    con = get_db()
    with con:
        data = con.execute(
            f"""SELECT * FROM {table_name} WHERE id == :id""", {"id": _id}
        ).fetchone()

        if not data:
            abort(404)

        con.execute(
            f"""UPDATE {table_name} SET {col_names_and_placeholder} WHERE id == :id""",
            values,
        )

    data = parse_single_db_data(data)
    prev_vals = list(data.items())

    log_msg = {
        "message": f"Values updated in home_improvements by {username}",
        "prev_values": prev_vals,
        "new_values": [("user_id", username)] + list(values.items()),
    }

    log_to_db(log_msg)
