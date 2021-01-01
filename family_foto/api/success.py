from typing import List

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from family_foto.errors import FamilyFotoServerError


def success_response(errors: List[FamilyFotoServerError]):
    """
    Returns a success response.
    """
    payload: dict = {'success': HTTP_STATUS_CODES.get(200)}
    if len(errors) > 0:
        payload.update({'error': [error.message for error in errors]})
    response = jsonify(payload)
    response.status_code = 200
    return response
