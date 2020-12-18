from flask_api import status
from flask_login import current_user

from family_foto import add_user, Role
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

    def test_request_sharing_with(self):
        """
        The post part of sharing photos of the settings route.
        """
        user_role = Role.query.filter_by(name='user').first()

        other_user = add_user('share_with_user', '123', [user_role])
        print(f'{other_user.id}')
        response = self.client.post('/settings', data=dict(share_with=[other_user.id]))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_change_password(self):
        """
        Tests if the password can be changed.
        """
        new_password = '4567'
        data = dict(old_password='1234', new_password=new_password,
                    repeat_new_password=new_password)
        response = self.client.post('/settings', data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(current_user.check_password(new_password))

    def test_change_password_unequal(self):
        """
        Tests the new password does not match.
        """
        new_password = '4567'
        old_password = '1234'
        data = dict(old_password=old_password, new_password=new_password,
                    repeat_new_password=new_password + '1')
        response = self.client.post('/settings', data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(current_user.check_password(old_password))
        self.assertFalse(current_user.check_password(new_password))

    def test_change_password_old_wrong(self):
        """
        Tests the new password does not match.
        """
        new_password = '4567'
        old_password = '1234'
        data = dict(old_password=old_password + '1', new_password=new_password,
                    repeat_new_password=new_password)
        response = self.client.post('/settings', data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(current_user.check_password(old_password))
        self.assertFalse(current_user.check_password(new_password))
