import logging
from typing import List

from app.service.home_improvements_service import (
    single_user_home_improvements,
    all_user_home_improvements,
    insert_home_improvements,
    delete_home_improvements,
    update_home_improvements,
)

logger = logging.getLogger(__name__)


def get_home_improvement() -> List[dict]:
    """Retrieves all home_improvement for the current user"""

    response = single_user_home_improvements()
    logger.debug("Retrieved Home Improvements")

    return response


def get_all_home_improvement() -> List[dict]:

    response = all_user_home_improvements()
    logger.debug("Retrieved All Home Improvements")

    return response


def add_home_improvement(body: dict) -> tuple:

    response = insert_home_improvements(body)
    logger.info("Home Improvement Added", extra={"data": response})

    return response, 201


def remove_home_improvement(id: int) -> tuple:

    delete_home_improvements(id)
    logger.info("Home Improvement Deleted", extra={"data": {"id": id}})

    return "", 204


def modify_home_improvement(body: dict) -> tuple:

    update_home_improvements(body)
    logger.info("Home Improvement Updated")

    return "", 204
