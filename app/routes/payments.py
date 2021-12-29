from app.controller.payments_controller import (
    single_user_payments,
    all_user_payments,
    insert_payment,
    delete_payment,
)


def get_payments():
    """Retrieves all payments for the current user"""

    response = single_user_payments()
    return response


def get_all_payments():

    response = all_user_payments()

    return response


def add_payment(body):

    insert_payment(body)

    return "", 204


def remove_payment(id):

    delete_payment(id)

    return "", 204
