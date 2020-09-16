from flask import Blueprint

api = Blueprint('api', __name__)

# avoid circular imports
from family_foto.api import errors, auth

