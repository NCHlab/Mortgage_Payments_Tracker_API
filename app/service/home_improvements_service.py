from typing import List

from app.core.session import get_session
from app.service.common import (
    get_from_table,
    get_all_from_table,
    insert_to_table,
    delete_from_table,
    update_table,
)


def single_user_home_improvements() -> List[dict]:
    return get_from_table("home_improvements")


def all_user_home_improvements() -> List[dict]:
    return get_all_from_table("home_improvements")


def insert_home_improvements(body: dict) -> None:

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

    insert_to_table(table_name, col_names, placeholder, values)


def delete_home_improvements(id: int) -> None:

    table_name = "home_improvements"
    delete_from_table(id, table_name)


def update_home_improvements(body: dict) -> None:

    get_session()

    _id = body["id"]
    table_name = "home_improvements"
    col_names_and_placeholder = (
        "paid = :paid, date = :date, reason = :reason, chargeable = :chargeable"
    )
    values = {
        "paid": body["paid"],
        "date": body["date"],
        "reason": body["reason"],
        "chargeable": body["chargeable"],
        "id": body["id"],
    }

    update_table(_id, table_name, col_names_and_placeholder, values)
