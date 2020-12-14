from flask import request
from flask_admin import BaseView, expose
from flask_login import current_user

from family_foto.logger import log
from family_foto.models import db
from family_foto.models.role import Role
from family_foto.models.user import User


class AdminPromoteView(BaseView):
    """
    View class for user role promotions.
    """

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        """
        Returns the template and has approval logic.
        """
        if request.method == 'POST':
            for user_id, role_name in request.form.to_dict().items():
                user = User.query.get(user_id)
                role = Role.query.filter_by(name=role_name).first()
                user.add_role(role)
                db.session.add(user)
                log.info(
                    f'{user.username} got role "{role.name}" added by {current_user.username}.')
            db.session.commit()

        return self.render('admin/promote.html', users=User.query.all(), roles=Role.query.all())
