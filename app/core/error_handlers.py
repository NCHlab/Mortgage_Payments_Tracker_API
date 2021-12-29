def method_not_allowed_405(err):
    response = {"error": "{}".format(err)}, 405
    return response


def method_not_allowed_400(err):
    response = {"error": "{}".format(err)}, 400
    return response


def method_not_allowed_401(err):
    response = {"error": "{}, bad token, or incorrect Auth Details".format(err)}, 401
    return response
