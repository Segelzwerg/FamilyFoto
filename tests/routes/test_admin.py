from flask_api import status

from tests.base_admin_test_case import BaseAdminTestCase
from tests.base_login_test_case import BaseLoginTestCase


class AdminAdminTestCase(BaseAdminTestCase):
    """
    Tests the route behind /admin with admin user.
    """

    def test_admin_route(self):
        """
        Test if the admin route can be reached.
        """
        response = self.client.get('/admin/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class AdminUserTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin as normal user
    """

    def test_admin_is_restricted(self):
        """
        Tests if a normal user can not view /admin
        """
        response = self.client.get('/admin/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class AdminAnonymousTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin as anonymous
    """

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
