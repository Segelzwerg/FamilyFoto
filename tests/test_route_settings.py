from flask_api import status

from tests.base_login_test_case import BaseLoginTestCase


class RouteSettingsTestCase(BaseLoginTestCase):
    """
    Tests the route of settings.
    """

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
