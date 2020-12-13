from flask import request
from flask_admin import BaseView, expose
from flask_login import current_user

from family_foto.forms.approval_form import ApprovalForm
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.approval import Approval
from family_foto.models.user import User


class AdminApprovalView(BaseView):
    """
    View class for user approval list.
    """

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        """
        Returns the template and has approval logic.
        """
        form = ApprovalForm()
        if request.method == 'POST':
            for approval_id in form.users.data:
                approval = Approval.query.get(approval_id)
                user = User.query.get(approval.user)
                user.approve()
                log.info(f'{user.username} got approved by {current_user.username}')
                Approval.query.filter_by(id=approval_id).delete()
                db.session.add(user)
            db.session.commit()
        form.users.choices = [(approval.id, User.query.filter_by(id=approval.user).first().username)
                              for approval in Approval.query.all()]
        return self.render('admin/approval.html', approval_form=form)
