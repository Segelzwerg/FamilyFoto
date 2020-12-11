from flask import request
from flask_admin import BaseView, expose

from family_foto.forms.approval_form import ApprovalForm
from family_foto.models import db
from family_foto.models.approval import Approval
from family_foto.models.user import User


class AdminApprovalView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = ApprovalForm()
        if request.method == 'POST':
            for approval_id in form.users.data:
                approval = Approval.query.get(approval_id)
                user = User.query.get(approval.user)
                user.approve()
                Approval.query.filter_by(id=approval_id).delete()
                db.session.add(user)
            db.session.commit()
        form.users.choices = [(approval.id, User.query.filter_by(id=approval.user).first().username)
                              for approval in Approval.query.all()]
        return self.render('admin/approval.html', approval_form=form)
