from abc import abstractmethod

from flask_admin import BaseView
from flask_login import current_user
from werkzeug.exceptions import abort


class AdminAccess(BaseView):
    @abstractmethod
    def index(self):
        raise NotImplementedError("This should be implemented by each view class separately.")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        abort(401)
