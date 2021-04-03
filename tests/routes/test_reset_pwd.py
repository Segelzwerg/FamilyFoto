from flask_api import status

from family_foto import add_user
from family_foto.models import db
from family_foto.models.reset_link import ResetLink
from family_foto.models.role import Role
from family_foto.models.user import User
from tests.base_test_case import BaseTestCase


class ResetPasswordTestCase(BaseTestCase):
    """
    Test the process of requesting and resetting the password.
    """

    def setUp(self):
        super().setUp()
        self.user_role = Role.query.filter_by(name='user').first()

        self.user = add_user('reseter', '123', [self.user_role])

        self.link = ResetLink.generate_link(user=self.user)
        self.reset_url = f'/reset-pwd/{self.user.id}/{self.link.link_hash}'
        db.session.commit()

    def test_reset_link(self):
        """
        Test if the link opens the reset form.
        """
        with self.client:
            response = self.client.get(self.reset_url)
            link: ResetLink = ResetLink.query.get(self.link.id)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertTrue(link.is_active())

    def test_reset_password(self):
        """
        Checks if the password can be changed.
        """
        with self.client:
            _ = self.client.get(self.reset_url)

            new_password = '1234'
            response = self.client.post(self.reset_url, data={'password': new_password,
                                                              'password_control': new_password},
                                        follow_redirects=True)
            user = User.query.get(self.user.id)

            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertTrue(user.check_password(new_password))

    def test_reset_wrong_id(self):
        """
        Tests if the password cannot be resetted with the wrong user id.
        """
        with self.client:
            _ = self.client.get(self.reset_url)

            new_password = '1234'
            _ = self.client.post(f'/reset-pwd/{self.user.id + 1}/{self.link.link_hash}',
                                 data={'password': new_password,
                                       'password_control': new_password},
                                 follow_redirects=True)
            user = User.query.get(self.user.id)

            self.assertFalse(user.check_password(new_password))

    def test_empty_hash(self):
        """
        Test that the hash link must be given.
        """
        with self.client:
            response = self.client.get(f'/reset-pwd/{self.user.id + 1}/')
            self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
