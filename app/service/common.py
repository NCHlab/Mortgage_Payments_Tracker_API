from app.core.utils import (
    get_session,
    log_to_db,
    parse_multi_db_data,
)
from app.core.db import get_db
from flask import abort


def user_data_from_table(table_name):

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


def all_user_data_from_table(table_name):

    # Only using to validate user is authenticated
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
