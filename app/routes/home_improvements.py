from app.service.home_improvements_service import (
    single_user_home_improvements,
    all_user_home_improvements,
    insert_home_improvements,
    delete_home_improvements,
    update_home_improvements,
)


def get_home_improvement():
    """Retrieves all home_improvement for the current user"""

    response = single_user_home_improvements()
    return response


def get_all_home_improvement():

    response = all_user_home_improvements()
    return response


def add_home_improvement(body):

    insert_home_improvements(body)
    return "", 204


def remove_home_improvement(id):

    delete_home_improvements(id)
    return "", 204


def modify_home_improvement(body):

    update_home_improvements(body)
    return "", 204
