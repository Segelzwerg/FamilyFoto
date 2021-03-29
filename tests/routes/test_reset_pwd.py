from flask_api import status

from family_foto.services.mail_service import mail
from tests.base_test_case import BaseTestCase


class ResetPasswordTestCase(BaseTestCase):
    """
    Test the process of requesting and resetting the password.
    """

    def test_reset_mail(self):
        """
        Tests if the mail with the reset link is in the outbox.
        """
        with mail.record_messages() as outbox, self.client:
            response = self.client.post('/reset-pwd', data={'username': 'marcel'},
                                        follow_redirects=True)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(1, len(outbox))
