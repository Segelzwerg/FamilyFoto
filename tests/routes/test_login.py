from flask_api import status
from flask_login import current_user

from tests.base_test_case import BaseTestCase


class LoginTestCase(BaseTestCase):
    """
    Tests the login functionality.
    """

    def test_login_page_is_available(self):
        """
        Checks if the login page can be reached.
        """
        with self.client:
            response = self.client.get('/login')
            self.assertTrue(status.is_success(response.status_code))

    def test_login(self):
        """
        Checks if the login work with correct credentials.
        """
        with self.client:
            response = self.client.post('/login',
                                        data={'username': 'marcel',
                                              'password': '1234'},
                                        follow_redirects=True)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(current_user.username, 'marcel')
            self.assertFalse(current_user.is_anonymous)

    def test_login_fails(self):
        """
        Checks that the login fails with wrong credentials.
        """
        with self.client:
            response = self.client.post('/login',
                                        data={'username': 'marcel',
                                              'password': '12345'},
                                        follow_redirects=True)
            self.assertTrue(status.is_success(response.status_code))
            self.assertTrue(current_user.is_anonymous)
