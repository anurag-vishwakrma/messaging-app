def public_endpoint(function):
    """
    For making API endpoint public .
    use public_endpoint decorator , to make endpoint accessible without access token.
    :param function:
    :return: function
    """
    function.is_public = True
    return function
