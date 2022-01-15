from typing import List

from app.service.overpayments_service import (
    single_user_overpayments,
    all_user_overpayments,
    insert_overpayment,
    delete_overpayment,
    update_overpayment,
)


def get_overpayments() -> List[dict]:
    """Retrieves all overpayments for the current user"""

    response = single_user_overpayments()
    return response


def get_all_overpayments() -> List[dict]:

    response = all_user_overpayments()
    return response


def add_overpayment(body: dict) -> tuple:

    response = insert_overpayment(body)
    return response, 201


def remove_overpayment(id: int) -> tuple:

    delete_overpayment(id)
    return "", 204


def modify_overpayment(body: dict) -> tuple:

    update_overpayment(body)
    return "", 204
