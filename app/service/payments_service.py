from app.core.utils import get_session
from app.service.common import (
    get_from_table,
    get_all_from_table,
    insert_to_table,
    delete_from_table,
    update_table,
)


def single_user_payments():
    return get_from_table("payments")


def all_user_payments():
    return get_all_from_table("payments")


def insert_payment(body):

    username = get_session()

    table_name = "payments"
    col_names = "user_id, paid, date, reason, from_tenant"
    placeholder = ":user_id, :paid, :date, :reason, :from_tenant"
    values = {
        "user_id": username,
        "paid": body["paid"],
        "date": body["date"],
        "reason": body["reason"],
        "from_tenant": body["from_tenant"],
    }

    insert_to_table(table_name, col_names, placeholder, values)


def delete_payment(id):

    table_name = "payments"
    delete_from_table(id, table_name)


def update_payment(body):

    get_session()

    _id = body["id"]
    table_name = "payments"
    col_names_and_placeholder = (
        "paid = :paid, date = :date, reason = :reason, from_tenant = :from_tenant"
    )
    values = {
        "paid": body["paid"],
        "date": body["date"],
        "reason": body["reason"],
        "from_tenant": body["from_tenant"],
        "id": body["id"],
    }

    update_table(_id, table_name, col_names_and_placeholder, values)
