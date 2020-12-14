from flask_api import status

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


class PromoteUserTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin as normal user
    """

    def test_admin_is_restricted(self):
        """
        Tests if a normal user can not view /admin
        """
        response = self.client.get('/admin/promote', follow_redirects=True)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class PromoteAnonymousTestCase(BaseLoginTestCase):
    """
    Test routes behind /admin as anonymous
    """

    def test_anonymous_has_no_access(self):
        """
        Test that anonymous user has not access.
        """
        self.patcher.stop()
        response = self.client.get('/admin/promote', follow_redirects=True)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
