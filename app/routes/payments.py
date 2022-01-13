from typing import List

from app.service.payments_service import (
    single_user_payments,
    all_user_payments,
    insert_payment,
    delete_payment,
    update_payment,
)


def get_payments() -> List[dict]:
    """Retrieves all payments for the current user"""

    response = single_user_payments()
    return response


def get_all_payments() -> List[dict]:

    response = all_user_payments()
    return response


def add_payment(body: dict) -> tuple:

    response = insert_payment(body)
    return response, 201


def remove_payment(id: int) -> tuple:

    delete_payment(id)
    return "", 204


def modify_payment(body: dict) -> tuple:

    update_payment(body)
    return "", 204
