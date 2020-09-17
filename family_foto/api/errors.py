from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code: int, message: str = None):
    """
    Returns json error response.
    :param status_code: http error code
    :param message: optional message
    """
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unkown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response
