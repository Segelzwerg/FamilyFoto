from functools import wraps

from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from family_foto.const import GUEST_LEVEL
from family_foto.errors import InActiveWarning
from family_foto.logger import log


def guest_user(func):
    """
    Annotation for checking if user is at least a guest user.
    :param func: the original function to annotate
    :return: of the original function or redirect
    """

    @wraps(func)
    def guest_user_wrapper(*args, **kwargs):
        """
        Wrapper of the original function
        :param args: arguments of the original function
        :param kwargs: key word arguments of the original function
        :return: return value of the original function
        """
        if current_user.is_authenticated and current_user.has_at_least_role(GUEST_LEVEL):
            return func(*args, **kwargs)
        return redirect(url_for('web.login'))

    return guest_user_wrapper


def is_active(func):
    """
    Annotation for checking if user is active.
    :param func: the original function to annotate
    :return: of the original function or redirect
    """

    @wraps(func)
    def is_active_wrapper(*args, **kwargs):
        """
        Wrapper of the original function
        :param args: arguments of the original function
        :param kwargs: key word arguments of the original function
        :return: return value of the original function
        """
        if current_user.is_authenticated and not current_user.active:
            message = 'This account is not activated yet. Please contact your admin.'
            log.warning(f'{current_user.username} tried to access content without being approved.')
            return render_template('index.html', user=current_user,
                                   w=InActiveWarning(message)), 302
            return redirect(url_for('web.index', ))
        return func(*args, **kwargs)

    return is_active_wrapper
