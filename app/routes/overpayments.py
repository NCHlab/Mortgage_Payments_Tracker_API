from app.service.overpayments_service import (
    single_user_overpayments,
    all_user_overpayments,
    insert_overpayment,
    delete_overpayment,
    update_overpayment,
)


def get_overpayments():
    """Retrieves all overpayments for the current user"""

    response = single_user_overpayments()
    return response


def get_all_overpayments():

    response = all_user_overpayments()

    return response


def add_overpayment(body):

    insert_overpayment(body)

    return "", 204


def remove_overpayment(id):

    delete_overpayment(id)

    return "", 204


def modify_overpayment(body):

    update_overpayment(body)

    return "", 204
