from flask_admin import BaseView, expose


class AdminApprovalView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/approval.html')
