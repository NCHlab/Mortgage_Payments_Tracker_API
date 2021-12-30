from app.core.utils import (
    get_session,
    log_to_db,
    parse_single_db_data,
    parse_multi_db_data,
)
from app.core.db import get_db
from flask import abort


def get_from_table(table_name):
    """
    Retrieves all data for the currently logged in individual for the specified table name
    """

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
    """
    Retrieves all data for the specified table name
    """

    # Using to validate user is authenticated
    get_session()

    c = get_db().cursor()
    c.execute(f"""SELECT * FROM {table_name}""")
    data = c.fetchall()

    if not data:
        return []

    list_of_payments = parse_multi_db_data(data)

    return list_of_payments


def insert_to_table(table_name, col_names, placeholder, values):
    """
    Inserts a row into a table for the specified table name
    """

    username = get_session()

    con = get_db()
    with con:
        con.execute(
            f"""INSERT INTO {table_name} ({col_names}) VALUES ({placeholder})""", values
        )

    log_msg = {
        "message": f"Values inserted into {table_name} by {username}",
        "values": values,
    }

    log_to_db(log_msg)


def delete_from_table(_id, table_name):
    """
    Deletes a row from a table for the specified id
    """

    username = get_session()
    con = get_db()

    with con:
        data = con.execute(
            f"""SELECT * FROM {table_name} WHERE id == :id""", {"id": _id}
        ).fetchone()

        if not data:
            abort(404)

        con.execute(f"""DELETE FROM {table_name} WHERE id == :id""", {"id": _id})

    values = parse_single_db_data(data)

    log_msg = {
        "message": f"Values deleted from {table_name} by {username}",
        "values": values,
    }

    log_to_db(log_msg)


def update_table(_id, table_name, col_names_and_placeholder, values):
    """
    Retrieves current table values, and sets new data to that id
    Logs both the previous and new values
    """

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

    prev_values = parse_single_db_data(data)

    values["user_id"] = username

    log_msg = {
        "message": f"Values updated in home_improvements by {username}",
        "prev_values": prev_values,
        "new_values": values,
    }

    log_to_db(log_msg)
