from flask_login import current_user
from werkzeug.exceptions import abort


def admin_user(func):
    """
    Decorator method for admin only access.
    :param func: function which should only be executable with admin privileges.
    :return: the return value of the function
    """

    # If some tries to access admin area it's more like it is an intruder than user,
    # so it's ok too simple abort.
    # pylint: disable=inconsistent-return-statement
    def wrapper(*arg, **kwargs):
        """
        Wraps the function with a check for adim privileges.
        :param arg: arguments of the original function
        :param kwargs: key word arguments of the original function
        :return: 401 or function value
        """
        if current_user.is_authenticated and current_user.has_role('admin'):
            result = func(*arg, **kwargs)
            return result
        abort(401)

    return wrapper
