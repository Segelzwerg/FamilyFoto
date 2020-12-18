from flask_admin import Admin

from family_foto.admin.admin_approval_view import AdminApprovalView
from family_foto.admin.admin_index_view import AdminHomeView
from family_foto.admin.admin_model_view import AdminModelView
from family_foto.admin.admin_promote_view import AdminPromoteView
from family_foto.models import db
from family_foto.models.file import File
from family_foto.models.role import Role
from family_foto.models.user import User


def create_admin(app) -> None:
    """
    Creates the admin area
    :param app: the current app needing an admin area
    """
    admin = Admin(app, name='FamilyFoto', template_mode='bootstrap4',
                  index_view=AdminHomeView(url='/admin'))  # lgtm [py/call-to-non-callable]
    admin.add_view(AdminModelView(User, db.session))  # lgtm [py/call-to-non-callable]
    admin.add_view(AdminModelView(File, db.session))  # lgtm [py/call-to-non-callable]
    admin.add_view(AdminModelView(Role, db.session))  # lgtm [py/call-to-non-callable]
    admin.add_view(AdminApprovalView(name='Approval',  # lgtm [py/call-to-non-callable]
                                     endpoint='approval'))  # lgtm [py/call-to-non-callable]
    admin.add_view(AdminPromoteView(name='Promotion',  # lgtm [py/call-to-non-callable]
                                    endpoint='promote'))  # lgtm [py/call-to-non-callable]
