import base64
from datetime import datetime
from unittest import mock

from family_foto.models.auth_token import AuthToken
from tests.base_test_case import BaseTestCase


def os_random_mock(size=24):
    return b'\x99\x9f\xa0\xb7\xdd\r\x9c#\x97\x0c\xae\xc1>b*\xdb\xde)Q=\xeb\xa7\x1b<'


class TestAuthTokenTestCase(BaseTestCase):
    """
    Test the AuthToken Class.
    """

    @mock.patch('family_foto.models.auth_token.datetime')
    def test_token_gen_expiration(self, mock_datetime):
        """
        Tests the token generator.
        """

        mock_datetime.utcnow = mock.Mock(return_value=datetime(1901, 12, 21))
        token = AuthToken.create_token(100)
        expected_expiration = datetime(1901, 12, 21, 0, 1, 40)
        self.assertEqual(expected_expiration, token.expiration)

    @mock.patch('family_foto.models.auth_token.os.urandom', side_effect=os_random_mock)
    def test_token_gen_token(self, os_random_mock):
        """
        Tests the token generator.
        """
        token = AuthToken.create_token(100)
        expected_token = base64.b64encode(os_random_mock()).decode('utf-8')
        self.assertEqual(expected_token, token.token)

    def test_token_check(self):
        """
        Test that a token is not expired.
        """
        token = AuthToken.create_token(300)
        self.assertTrue(token.check(), msg=f'{token} should not have expired yet.')

    @mock.patch('family_foto.models.auth_token.datetime')
    def test_token_expired(self, mock_datetime):
        """
        Test token is actually expired.
        """
        mock_datetime.utcnow = mock.Mock(return_value=datetime(1901, 12, 21))
        token = AuthToken.create_token(100)
        mock_datetime.utcnow = mock.Mock(return_value=datetime(1901, 12, 21, 0, 1, 50))
        self.assertFalse(token.check())

    def test_revoke_token(self):
        """
        Tests if a token can be revoked.
        """
        token = AuthToken.create_token(6000)
        token.revoke()
        self.assertFalse(token.check(), msg=f'{token} is still valid.')
