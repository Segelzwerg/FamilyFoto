from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from family_foto.errors import FamilyFotoServerError


def success_response(error: FamilyFotoServerError):
    """
    Returns a success response.
    """
    payload: dict = {'success': HTTP_STATUS_CODES.get(200)}
    if error:
        payload.update({'error': error.message})
    response = jsonify(payload)
    response.status_code = 200
    return response
