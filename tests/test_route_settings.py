from unittest.mock import patch

from flask_api import status

from family_foto.models.user import User
from tests.base_test_case import BaseTestCase


class RouteSettingsTestCase(BaseTestCase):
    """
    Tests the route of settings.
    """
    def setUp(self):
        super().setUp()
        self.patcher = patch('flask_login.utils._get_user')
        self.mock_current_user = self.patcher.start()
        self.mock_current_user.return_value = User(id=1,
                                                   username='marcel')

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()

    def test_settings_route(self):
        """
        Tests the user settings route.
        """
        response = self.client.get('/settings')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_require_login_settings(self):
        """
        Tests that an user must be logged in to see the settings page.
        """
        self.patcher.stop()
        response = self.client.get('/settings')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
