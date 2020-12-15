from flask_api import status

from family_foto import add_user, Role
from family_foto.models import db
from family_foto.models.approval import Approval
from tests.base_admin_test_case import BaseAdminTestCase
from tests.base_login_test_case import BaseLoginTestCase


class TestUserApproval(BaseAdminTestCase):
    """
    Tests the approval of the admin for new users.
    """

    def test_route(self):
        """
        Tests the route /admin/approval exists.
        """
        with self.client:
            response = self.client.get('/admin/approval', follow_redirects=True)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_approval_accept(self):
        """
        Tests if an approval accepting works,
        """
        new_user = add_user('approve', 'no', [Role.query.filter_by(name='guest').first()])
        new_user_approval = Approval(id=1, user=new_user.id)
        db.session.add(new_user_approval)
        db.session.commit()
        with self.client:
            data = dict(users=['1'], submit=True)
            response = self.client.post('/admin/approval', data=data, follow_redirects=True)
            self.assertEqual(0, len(Approval.query.all()))
            self.assertEqual(True, new_user.is_active)
            self.assertEqual(status.HTTP_200_OK, response.status_code)


class ApprovalUserTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin/approval as normal user
    """

    def test_admin_is_restricted(self):
        """
        Tests if a normal user can not view /admin
        """
        response = self.client.get('/admin/approval', follow_redirects=True)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class ApprovalAnonymousTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin as anonymous
    """

    def test_anonymous_has_no_access(self):
        """
        Test that anonymous user has not access.
        """
        self.patcher.stop()
        response = self.client.get('/admin/approval', follow_redirects=True)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
