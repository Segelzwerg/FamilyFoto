from flask import Blueprint, jsonify, request, current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_login import current_user

from family_foto.api.errors import error_response
from family_foto.api.success import success_response
from family_foto.logger import log
from family_foto.models.auth_token import AuthToken
from family_foto.models.user import User
from family_foto.services.upload_service import UploadService

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
    user = current_user if current_user.is_authenticated else User.query.get(token.user_id)
    log.info(f'{user} requested AuthToken.')
    return jsonify(token.to_dict())


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
        log.info(f'{user} logged in via API.')
        return user
    log.warning(f'Wrong password for {user.username} from API.')
    return None


@basic_auth.error_handler
def basic_auth_error(status):
    """
    Returns the custom error message for a given error code.
    :param status: integer of the error code
    """
    log.warning(status)
    return error_response(status)


@token_auth.verify_token
def verify_token(token: [AuthToken, str]):
    """
    Verifies the current token.
    :param token: token to validate
    """
    if isinstance(token, str):
        token = AuthToken.query.filter_by(token=token).first()
    if user_id := request.headers.get('USER_ID'):
        return token.check(int(user_id)) if token else None
    log.warning(f'Requested token for user with id {user_id} is invalid.')
    return None


@token_auth.error_handler
def token_auth_error(status: int):
    """
    Handles token auth errors
    :param status: http error status code
    """
    return error_response(status)


@api_bp.route('/upload', methods=['POST'])
@token_auth.login_required
def upload():
    """
    Uploads files via api.
    """
    files = request.files.getlist('files')
    if user_id := request.headers.get('USER_ID'):
        user_id = int(user_id)
    app = current_app._get_current_object()
    uploader = UploadService(files, user_id, app)
    upload_errors = uploader.upload()
    return success_response(upload_errors)
