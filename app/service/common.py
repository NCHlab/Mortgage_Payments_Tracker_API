from flask import abort
from typing import List

import logging

from app.core.session import get_session
from app.core.db_log import log_to_db
from app.core.parsers import parse_single_db_data, parse_multi_db_data
from app.core.db import get_db

logger = logging.getLogger(__name__)


def get_from_table(table_name: str) -> List[dict]:
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

    logger.debug(list_of_payments)

    return list_of_payments


def get_all_from_table(table_name: str) -> List[dict]:
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

    logger.debug(list_of_payments)

    return list_of_payments


def insert_to_table(
    table_name: str, col_names: str, placeholder: str, values: dict
) -> dict:
    """
    Inserts a row into a table for the specified table name
    """

    username = get_session()

    c = get_db().cursor()
    c.execute(
        f"""INSERT INTO {table_name} ({col_names}) VALUES ({placeholder})""", values
    )
    last_id = c.lastrowid

    log_msg = {
        "message": f"Values inserted into {table_name} by {username}",
        "state": "INSERT",
        "new_values": values,
    }

    log_to_db(log_msg, table_name, "INSERT")
    logger.info(log_msg)

    return {"id": last_id, **values}


def delete_from_table(_id: int, table_name: str) -> None:
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
        "state": "DELETE",
        "prev_values": values,
    }

    log_to_db(log_msg, table_name, "DELETE")
    logger.info(log_msg)


def update_table(
    _id: int, table_name: str, col_names_and_placeholder: str, values: dict
) -> None:
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
        "message": f"Values updated in {table_name} by {username}",
        "state": "UPDATE",
        "prev_values": prev_values,
        "new_values": values,
    }

    log_to_db(log_msg, table_name, "UPDATE")
    logger.info(log_msg)


def get_db_sum_payments(table_name: str, username=None) -> dict:

    session_username = get_session()
    if not username:
        username = session_username

    con = get_db()

    field_name = table_name

    with con:
        data = con.execute(
            f"""SELECT sum(paid) as {field_name} FROM {table_name} WHERE user_id == :id""",
            {"id": username},
        ).fetchone()

        if not data:
            return {}

    data = parse_single_db_data(data)

    return data


def get_all_users():

    c = get_db().cursor()
    c.execute("""SELECT username FROM users;""")
    data = c.fetchall()

    if not data:
        return []

    list_of_data = parse_multi_db_data(data)

    return list_of_data


def get_custom_query(query: str) -> List[dict]:
    get_session()

    c = get_db().cursor()
    c.execute(query)
    data = c.fetchall()

    if not data:
        return []

    list_of_data = parse_multi_db_data(data)

    return list_of_data


def strip_out_field(data, field):

    for obj in data:
        try:
            del obj[field]
        except KeyError:
            continue

    return data
