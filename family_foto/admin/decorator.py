from flask import request
from werkzeug.exceptions import abort

from family_foto.models.user import User


def admin_auth(func):
    """
    Decorator method for admin authentication.
    :param func: function which should only be executable with admin privileges.
    :return: the return value of the function
    """

    # If some tries to access admin area it's more like it is an intruder than user,
    # so it's ok too simple abort.
    # pylint: disable=inconsistent-return-statements
    def wrapper(*arg, **kwargs):
        """
        Wraps the function with a check for admin privileges.
        :param arg: arguments of the original function
        :param kwargs: key word arguments of the original function
        :return: 401 or function value
        """
        if request.authorization:
            username = request.authorization.username
            password = request.authorization.password
            admin: User = User.query.filter_by(username=username).first()
            if username == 'admin' and admin.check_password(password):
                result = func(*arg, **kwargs)
                return result
        abort(401)

    return wrapper
