from flask import Blueprint, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from family_foto.api.errors import error_response
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.auth_token import AuthToken
from family_foto.models.user import User

api_bp = Blueprint('api', __name__, url_prefix='/api')

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@api_bp.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    """
    Retrieves a new token or the current one.
    :return: an AuthToken in a json
    """
    token = basic_auth.current_user().get_token()
    db.session.commit()
    log.info(f'{current_user} requested AuthToken.')
    return jsonify({'token': token.to_dict()})


@basic_auth.verify_password
def verify_password(username: str, password: str) -> [None, User]:
    """
    Verifies the password for given user.
    :param username: the username string
    :param password: the password string
    :return: the user object
    """
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


@basic_auth.error_handler
def basic_auth_error(status):
    """
    Returns the custom error message for a given error code.
    :param status: integer of the error code
    """
    return error_response(status)


@token_auth.verify_token
def verify_token(token: AuthToken):
    """
    Verifies the current token.
    :param token: token to validate
    """
    return token.check(current_user.id) if token else None


@token_auth.error_handler
def token_auth_error(status: int):
    """
    Handles token auth errors
    :param status: http error status code
    """
    return error_response(status)


@api_bp.route('/upload', methods=['POST'])
@token_auth.login_required
def upload_file(files: [FileStorage]):
    """
    Uploads files via api.
    """
    for file in files:
        upload_file(file)
