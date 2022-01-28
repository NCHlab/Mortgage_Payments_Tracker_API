import logging
from typing import List

from app.service.payments_service import (
    single_user_payments,
    all_user_payments,
    insert_payment,
    delete_payment,
    update_payment,
)

logger = logging.getLogger(__name__)


def get_payments() -> List[dict]:
    """Retrieves all payments for the current user"""

    response = single_user_payments()
    logger.debug("Retrieved Payments")

    return response


def get_all_payments() -> List[dict]:

    response = all_user_payments()
    logger.debug("Retrieved All Payments")

    return response


def add_payment(body: dict) -> tuple:

    response = insert_payment(body)
    logger.info("Payment Added", extra={"data": response})

    return response, 201


def remove_payment(id: int) -> tuple:

    delete_payment(id)
    logger.info("Payment Deleted", extra={"data": {"id": id}})

    return "", 204


def modify_payment(body: dict) -> tuple:

    update_payment(body)
    logger.info("Payment Updated")

    return "", 204
