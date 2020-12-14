from flask_admin import expose, AdminIndexView

from family_foto.admin.admin_access import AdminAccess


class AdminHomeView(AdminAccess, AdminIndexView):
    """
    The home view for the admin.
    """

    @expose('/')
    def index(self):
        return self.render('/admin/index.html')
