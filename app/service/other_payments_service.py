from typing import List

from app.core.session import get_session
from app.service.common import (
    get_from_table,
    get_all_from_table,
    insert_to_table,
    delete_from_table,
    update_table,
)


def single_user_other_payments() -> List[dict]:
    return get_from_table("other_payments")


def all_user_other_payments() -> List[dict]:
    return get_all_from_table("other_payments")


def insert_other_payments(body: dict) -> None:

    username = get_session()

    table_name = "other_payments"
    col_names = "user_id, paid, chargeable, date, reason"
    placeholder = ":user_id, :paid, :chargeable, :date, :reason"
    values = {
        "user_id": username,
        "paid": body["paid"],
        "chargeable": body["chargeable"],
        "date": body["date"],
        "reason": body["reason"],
    }

    inserted_data = insert_to_table(table_name, col_names, placeholder, values)

    return inserted_data


def delete_other_payments(id: int) -> None:

    table_name = "other_payments"
    delete_from_table(id, table_name)


def update_other_payments(body: dict) -> None:

    get_session()

    _id = body["id"]
    table_name = "other_payments"
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
