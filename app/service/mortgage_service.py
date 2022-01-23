from typing import List

from app.core.db import get_db
from app.core.parsers import parse_single_db_data
from app.service.common import get_db_sum_payments, get_all_users


def mortgage_info() -> dict:
    c = get_db().cursor()

    c.execute(
        f"""SELECT mortgage.provider, mortgage.loan, mortgage.interest_rate, mortgage.period, mortgage.start_period,
            mortgage_balance.balance, mortgage_balance.date_updated
            FROM mortgage
            INNER JOIN mortgage_balance ON mortgage.provider = mortgage_balance.provider
            WHERE mortgage.active = :active
            ORDER BY mortgage_balance.date_updated DESC LIMIT 1;
        """,
        {"active": True},
    )

    data = c.fetchone()

    if not data:
        return {}

    data = parse_single_db_data(data)

    return data


def aggregate_user_payments() -> dict:

    payments = get_db_sum_payments("payments")
    overpayments = get_db_sum_payments("overpayments")
    home_improvements = get_db_sum_payments("home_improvements")

    data = {**payments, **overpayments, **home_improvements}
    return data


def aggregate_all_user_payments() -> List[dict]:

    all_users = get_all_users()

    data = []

    for user in all_users:
        payments = get_db_sum_payments("payments", user["username"])
        overpayments = get_db_sum_payments("overpayments", user["username"])
        home_improvements = get_db_sum_payments("home_improvements", user["username"])

        single_user_data = {**payments, **overpayments, **home_improvements}
        data.append({user["username"]: single_user_data})

    return data
