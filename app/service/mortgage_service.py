from app.core.db import get_db
from app.core.utils import parse_single_db_data


def mortgage_info():
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
