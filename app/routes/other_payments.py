import logging
from typing import List

from app.service.other_payments_service import (
    single_user_other_payments,
    all_user_other_payments,
    insert_other_payments,
    delete_other_payments,
    update_other_payments,
)

logger = logging.getLogger(__name__)


def get_other_payment() -> List[dict]:
    """Retrieves all other_payment for the current user"""

    response = single_user_other_payments()
    logger.debug("Retrieved Other Payments")

    return response


def get_all_other_payment() -> List[dict]:

    response = all_user_other_payments()
    logger.debug("Retrieved All Other Payments")

    return response


def add_other_payment(body: dict) -> tuple:

    response = insert_other_payments(body)
    logger.info("Other Payment Added", extra={"data": response})

    return response, 201


def remove_other_payment(id: int) -> tuple:

    delete_other_payments(id)
    logger.info("Other Payment Deleted", extra={"data": {"id": id}})

    return "", 204


def modify_other_payment(body: dict) -> tuple:

    update_other_payments(body)
    logger.info("Other Payment Updated")

    return "", 204
