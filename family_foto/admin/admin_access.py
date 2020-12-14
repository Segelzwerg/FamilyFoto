from abc import abstractmethod

from flask_admin import BaseView
from flask_login import current_user
from werkzeug.exceptions import abort


class AdminAccess(BaseView):
    """
    Gate keeper for admin only,
    """

    @abstractmethod
    def index(self):
        """
        Raises error because this is abstract.
        """
        raise NotImplementedError("This should be implemented by each view class separately.")

    def is_accessible(self):
        """
        Checks if user has admin role.
        """
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        """
        Aborts if not admin.
        """
        abort(401)
