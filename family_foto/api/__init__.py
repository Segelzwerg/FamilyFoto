from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

# avoid circular imports
# pylint: disable=wrong-import-position
from family_foto.api import errors, auth
