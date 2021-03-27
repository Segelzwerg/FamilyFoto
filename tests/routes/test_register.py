from flask_api import status

from family_foto.models.user import User
from tests.base_test_case import BaseTestCase
from tests.test_utils.mocking import mock_user


class RegisterTestCase(BaseTestCase):
    """
    Tests the route behind /register.
    """

    def test_register_is_available(self):
        """
        Checks if the register page can be reached.
        """
        with self.client:
            response = self.client.get('/register')
            self.assertTrue(status.is_success(response.status_code))

    def test_register_a_guest_user(self):
        """
        Checks if it is possible to register a new user.
        """
        with self.client:
            response = self.client.post('register',
                                        data={'username': 'Lea',
                                              'password': '1234',
                                              'password_control': '1234'})
            user = User.query.filter_by(username='Lea').first()
            self.assertEqual(status.HTTP_302_FOUND, response.status_code)
            self.assertIsNotNone(user)

    def test_register_password_not_matching(self):
        """
        Checks if the user is returned to the register page.
        """
        with self.client:
            response = self.client.post('register',
                                        data={'username': 'Lea',
                                              'password': '1234',
                                              'password_control': '4321'})
            user = User.query.filter_by(username='Lea').first()
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertIsNone(user)

    def test_redirect_with_authenticated_user(self):
        """
        Checks if an authenticated user is redirected to index.
        """
        mock_user(self, 'marcel', 'user')
        with self.client:
            response = self.client.get('/register')
            self.patcher.stop()
            self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_register_a_guest_user_with_email(self):
        """
        Checks if it is possible to register a new user with an email address.
        """
        with self.client:
            response = self.client.post('register',
                                        data={'username': 'Lea',
                                              'email': 'lea@haas.com',
                                              'password': '1234',
                                              'password_control': '1234'})
            user = User.query.filter_by(username='Lea').first()
            self.assertEqual(status.HTTP_302_FOUND, response.status_code)
            self.assertIsNotNone(user)
