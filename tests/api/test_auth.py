from base64 import b64encode

from flask_api import status
from flask_login import current_user

from family_foto.api.auth import verify_token
from family_foto.models.auth_token import AuthToken
from tests.base_login_test_case import BaseLoginTestCase


class ApiAuthTestCase(BaseLoginTestCase):
    """
    Tests the api.
    """

    def test_token_getter(self):
        """
        Tests the api route for getting a token.
        """
        with self.client:
            credentials = b64encode(b'marcel:1234').decode('utf-8')
            response = self.client.post('/api/token',
                                        headers={'Authorization': f'Basic {credentials}'})

            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_wrong_password(self):
        """
        Tests the error handling of wrong credentials.
        """
        with self.client:
            credentials = b64encode(b'marcel:12345').decode('utf-8')
            response = self.client.post('/api/token',
                                        headers={'Authorization': f'Basic {credentials}'})

            self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_verify_token(self):
        """
        Tests the verification of a token.
        """
        token = AuthToken.create_token(current_user)
        self.assertTrue(verify_token(token), msg=f'Expected {token} to be verified but was not.')
