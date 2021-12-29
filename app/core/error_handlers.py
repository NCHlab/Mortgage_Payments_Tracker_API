def method_not_allowed_400(err):
    response = {"error": "{}".format(err)}, 400
    return response


def method_not_allowed_401(err):
    response = {"error": "{}, bad token, or incorrect Auth Details".format(err)}, 401
    return response


def method_not_allowed_404(err):
    response = {
        "error": "{}".format("The Resource does not exist or Request URL was not found")
    }, 404
    return response


def method_not_allowed_405(err):
    response = {"error": "{}".format(err)}, 405
    return response
