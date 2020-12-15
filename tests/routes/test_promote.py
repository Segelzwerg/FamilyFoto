from flask_api import status

from family_foto.models.role import Role
from family_foto.utils.add_user import add_user
from tests.base_admin_test_case import BaseAdminTestCase
from tests.base_login_test_case import BaseLoginTestCase


class PromoteTestCase(BaseAdminTestCase):
    """
    Test promotion of users.
    """

    def test_route(self):
        """
        Tests the route exists.
        """
        response = self.client.get('/admin/promote/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_promotion(self):
        """
        Tests if the promotion does work.
        """
        guest_role = Role.query.filter_by(level=2).first()
        user = add_user('dummy', 'no', [guest_role])
        data = {user.id: 'admin'}
        response = self.client.post('/admin/promote', data=data, follow_redirects=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(user.has_at_least_role(1))


class PromoteUserTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin as normal user
    """

    def test_admin_is_restricted(self):
        """
        Tests if a normal user can not view /admin/promote
        """
        response = self.client.get('/admin/promote', follow_redirects=True)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class PromoteAnonymousTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin/promote as anonymous
    """

    def test_anonymous_has_no_access(self):
        """
        Test that anonymous user has not access.
        """
        self.patcher.stop()
        response = self.client.get('/admin/promote', follow_redirects=True)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
