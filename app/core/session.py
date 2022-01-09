from flask import session, abort


def get_session():
    """
    Retrieves the user_id for the user accessing the session
    Works as an Authentication system to ensure their session is valid
    """

    username = session.get("user_id")

    if not username:
        abort(401)

    return username
