from flask_api import status

from tests.base_login_test_case import BaseLoginTestCase


class AdminTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin
    """

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
