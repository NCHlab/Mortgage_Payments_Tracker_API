from app.core.utils import get_session
from app.service.mortgage_service import mortgage_info


def get_mortgage():
    get_session()

    response = mortgage_info()

    return response
