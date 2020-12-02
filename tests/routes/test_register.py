from flask_api import status

from family_foto import User
from tests.base_test_case import BaseTestCase


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
            self.assertEqual(status.HTTP_200_OK, response.status_code)
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
