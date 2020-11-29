from flask_admin import AdminIndexView, expose
from flask_login import current_user
from werkzeug.exceptions import abort


class AdminHomeView(AdminIndexView):
    """
    The home view for the admin.
    """
    @expose('/')
    def index(self):
        return self.render('/admin/index.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        abort(401)
