from unittest.mock import patch

from flask_api import status

from family_foto import Role, add_user
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_test_case import BaseTestCase


class AdminAdminTestCase(BaseTestCase):
    """
    Tests the route behind /admin with admin user.
    """

    def setUp(self):
        super().setUp()
        self.patcher = patch('flask_login.utils._get_user')
        self.mock_current_user = self.patcher.start()
        user_role = Role.query.filter_by(name='admin').first()
        user = add_user('admin', '1234', [user_role])
        self.mock_current_user.return_value = user
        self.mock_current_user.id = user.id

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()

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
