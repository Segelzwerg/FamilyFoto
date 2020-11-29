import flask_admin.contrib.sqla
from flask_login import current_user
from werkzeug.exceptions import abort


class AdminModelView(flask_admin.contrib.sqla.ModelView):
    """
    Model view of database entries.
    """

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        abort(401)
