from app.core.utils import get_session
from app.service.mortgage_service import mortgage_info, aggregate_user_payments


def get_mortgage():
    get_session()

    response = mortgage_info()

    return response


def get_aggregate():
    get_session()

    response = aggregate_user_payments()

    return response
