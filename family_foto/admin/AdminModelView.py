import flask_admin.contrib.sqla
from flask_login import current_user
from werkzeug.exceptions import abort


class AdminModelView(flask_admin.contrib.sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.has_role('admin') and
                current_user.is_active)

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect to send 401.
        """
        if not self.is_accessible():
            abort(401)
