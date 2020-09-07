from flask_api import status
from flask_login import current_user

from tests.base_test_case import BaseTestCase


class LogoutTestCase(BaseTestCase):
    """
    Test case for user logouts.
    """

    def test_users_can_logout(self):
        """
        Tests if user can logout.
        """

        with self.client:
            self.client.post('/login',
                             data={'username': 'marcel',
                                   'password': '1234'},
                             follow_redirects=True)
            response = self.client.get('/logout')

            username = current_user.username if not current_user.is_anonymous else 'anonymous'
            self.assertTrue(current_user.is_anonymous, msg=f'user <{username}> is '
                                                           f'still logged in')
            self.assertTrue(status.is_redirect(response.status_code))
