from typing import List

from app.core.session import get_session
from app.service.common import (
    get_from_table,
    get_all_from_table,
    insert_to_table,
    delete_from_table,
    update_table,
)


def single_user_overpayments() -> List[dict]:
    return get_from_table("overpayments")


def all_user_overpayments() -> List[dict]:
    return get_all_from_table("overpayments")


def insert_overpayment(body: dict) -> None:

    username = get_session()

    table_name = "overpayments"
    col_names = "user_id, paid, date, reason"
    placeholder = ":user_id, :paid, :date, :reason"
    values = {
        "user_id": username,
        "paid": body["paid"],
        "date": body["date"],
        "reason": body["reason"],
    }

    inserted_data = insert_to_table(table_name, col_names, placeholder, values)

    return inserted_data


def delete_overpayment(id: int) -> None:

    table_name = "overpayments"

    delete_from_table(id, table_name)


def update_overpayment(body: dict) -> None:

    get_session()

    _id = body["id"]
    table_name = "overpayments"
    col_names_and_placeholder = "paid = :paid, date = :date, reason = :reason"
    values = {
        "paid": body["paid"],
        "date": body["date"],
        "reason": body["reason"],
        "id": body["id"],
    }

    update_table(_id, table_name, col_names_and_placeholder, values)
