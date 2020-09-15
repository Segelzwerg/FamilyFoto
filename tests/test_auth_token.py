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
