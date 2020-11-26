from flask_api import status

from tests.base_login_test_case import BaseLoginTestCase


class AdminTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin
    """

    def test_admin_is_restricted(self):
        """
        Tests if a normal user can not view /admin
        """

        response = self.client.get('/admin')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_anonymous_has_no_access(self):
        """
        Test that anonymous user has not access.
        """
        self.patcher.stop()
        response = self.client.get('/admin/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
