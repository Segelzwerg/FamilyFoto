from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def success_response():
    payload = {'success': HTTP_STATUS_CODES.get(200)}
    response = jsonify(payload)
    response.status_code = 200
    return response
