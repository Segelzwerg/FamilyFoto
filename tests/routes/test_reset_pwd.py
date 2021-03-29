from flask_api import status

from family_foto import add_user
from family_foto.models import db
from family_foto.models.reset_link import ResetLink
from family_foto.models.role import Role
from family_foto.models.user import User
from family_foto.services.mail_service import mail
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

    def test_reset_mail(self):
        """
        Tests if the mail with the reset link is in the outbox.
        """
        with mail.record_messages() as outbox, self.client:
            response = self.client.post('/reset-pwd', data={'username': 'marcel'},
                                        follow_redirects=True)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(1, len(outbox))

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
