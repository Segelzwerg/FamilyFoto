from flask_api import status

from family_foto import Role
from tests.base_login_test_case import BaseLoginTestCase


class AdminTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin
    """

    def test_admin_route(self):
        """
        Test if the admin route can be reached.
        """
        admin_role = Role.query.filter_by(name='admin')
        self.mock_current_user.role = [admin_role]
        response = self.client.get('/admin/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_admin_is_restricted(self):
        """
        Tests if a normal user can not view /admin
        """
        response = self.client.get('/admin/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_anonymous_has_no_access(self):
        """
        Test that anonymous user has not access.
        """
        self.patcher.stop()
        response = self.client.get('/admin/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_anonymous_has_no_access_user(self):
        """
        Test that anonymous user has not access.
        """
        self.patcher.stop()
        response = self.client.get('/admin/user/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_anonymous_has_no_access_role(self):
        """
        Test that anonymous user has not access.
        """
        self.patcher.stop()
        response = self.client.get('/admin/role/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_anonymous_has_no_access_file(self):
        """
        Test that anonymous user has not access.
        """
        self.patcher.stop()
        response = self.client.get('/admin/file/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
