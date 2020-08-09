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
            response = self.client.post('/login',
                                        data={'username': 'marcel',
                                              'password': '1234'},
                                        follow_redirects=True)
            self.client.get('/logout')

            self.assertTrue(current_user.is_anonymous, msg=f'user <{current_user.username}> is '
                                                           f'still logged in')
