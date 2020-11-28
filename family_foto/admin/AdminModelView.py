import flask_admin.contrib.sqla
from flask import url_for
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect


class AdminModelView(flask_admin.contrib.sqla.ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        abort(401)
        return redirect(url_for('index.html'))
