from flask_httpauth import HTTPBasicAuth

from family_foto.api.errors import error_response
from family_foto.models.user import User

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username: str, password: str) -> User:
    """
    Verifies the password for given user.
    :param username: the username string
    :param password: the password string
    :return: the user object
    """
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    """
    Returns the custom error message for a given error code.
    :param status: integer of the error code
    """
    return error_response(status)
