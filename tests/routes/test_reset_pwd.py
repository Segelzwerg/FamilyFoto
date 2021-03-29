from flask_api import status

from family_foto import add_user, Role
from family_foto.models.reset_link import ResetLink
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
        link = ResetLink.generate_link(user=self.user)
        with self.client:
            reset_url = f'/reset-pwd/{self.user.id}/{link.link_hash}'
            response = self.client.get(reset_url)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
