from datetime import datetime
from typing import List

from app.service.common import get_custom_query, strip_out_field
from app.core.query_builder import (
    query_extractor,
    query_formatter,
    query_builder,
    date_limit_builder,
)


def db_log_payment_service(
    tablename: str, state: str, less_than: bool, date: str, limit: str
) -> List[dict]:

    if date is None:
        date = str(datetime.now().isoformat())

    if limit is None:
        limit = 10

    tablename = query_extractor(tablename)
    state = query_extractor(state)

    table_query = query_formatter(
        tablename, ["payments", "overpayments", "other_payments"]
    )
    state_query = query_formatter(state, ["INSERT", "UPDATE", "DELETE"])

    final_query = query_builder(table_query, state_query, less_than, date, limit)

    data = get_custom_query(final_query)

    return data


def db_log_login_service(less_than: bool, date: str, limit: str) -> List[dict]:

    if date is None:
        date = str(datetime.now().isoformat())

    if limit is None:
        limit = 10

    final_query = f"""SELECT * FROM logs WHERE state IS "LOGIN" """
    final_query = date_limit_builder(final_query, less_than, date, limit)

    data = get_custom_query(final_query)
    data = strip_out_field(data, "table_name")

    return data
