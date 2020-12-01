from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect

from family_foto import Role


def guest_user(func):
    """
    Annotation for checking if user is at least a guest user.
    :param func: the original function to annotate
    :return: of the original function or redirect
    """

    def wrapper(*args, **kwargs):
        """
        Wrapper of the original function
        :param args: arguments of the original function
        :param kwargs: key word arguments of the original function
        :return: return value of the original function
        """
        guest_role = Role.query.filter_by(name='guest').first()
        if current_user.is_authenticated and current_user.has_at_least_role(guest_role.level):
            return func(*args, **kwargs)
        return redirect(url_for('web.login'))

    return wrapper