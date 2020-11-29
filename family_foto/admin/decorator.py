from flask_login import current_user
from werkzeug.exceptions import abort


def admin_user(func):
    def wrapper(*arg, **kwargs):
        if current_user.is_authenticated and current_user.has_role('admin'):
            result = func(*arg, **kwargs)
            return result
        abort(401)

    return wrapper
