from app.core.session import get_session
from app.service.mortgage_service import mortgage_info, aggregate_user_payments


def get_mortgage() -> dict:
    get_session()

    response = mortgage_info()

    return response


def get_aggregate() -> dict:
    get_session()

    response = aggregate_user_payments()

    return response
