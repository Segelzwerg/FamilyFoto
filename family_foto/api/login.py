from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user

from family_foto.api import api
from family_foto.api.errors import error_response
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.user import User

basic_auth = HTTPBasicAuth()


@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    """
    Retrieves a new token or the current one.
    :return: an AuthToken in a json
    """
    token = basic_auth.current_user().get_token()
    db.session.commit()
    log.info(f'{current_user} requested AuthToken.')
    return jsonify({'token': token})


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
