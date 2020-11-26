import base64
from datetime import datetime
from unittest import mock

from family_foto import add_user, Role
from family_foto.models.auth_token import AuthToken
from tests.base_test_case import BaseTestCase


# requires parameter for mocking
# pylint: disable=W0613
def mock_os_random(size=24):
    """
    Mocks the os random function
    :param size:
    """
    return b'\x99\x9f\xa0\xb7\xdd\r\x9c#\x97\x0c\xae\xc1>b*\xdb\xde)Q=\xeb\xa7\x1b<'


class TestAuthTokenTestCase(BaseTestCase):
    """
    Test the AuthToken Class.
    """

    def setUp(self):
        super().setUp()
        user_role = Role.query.filter_by(name='user').first()

        self.user = add_user('authy', 'secret', [user_role])

    @mock.patch('family_foto.models.auth_token.datetime')
    def test_token_gen_expiration(self, mock_datetime):
        """
        Tests the token generator.
        """

        mock_datetime.utcnow = mock.Mock(return_value=datetime(1901, 12, 21))
        token = AuthToken.create_token(self.user, 100)
        expected_expiration = datetime(1901, 12, 21, 0, 1, 40)
        self.assertEqual(expected_expiration, token.expiration)

    @mock.patch('family_foto.models.auth_token.os.urandom', side_effect=mock_os_random)
    def test_token_gen_token(self, os_random_mock):
        """
        Tests the token generator.
        """
        token = AuthToken.create_token(self.user, 100)
        expected_token = base64.b64encode(os_random_mock()).decode('utf-8')
        self.assertEqual(expected_token, token.token)

    def test_token_check(self):
        """
        Test that a token is not expired.
        """
        token = AuthToken.create_token(self.user, 300)
        self.assertTrue(token.check(self.user.id), msg=f'{token} should not have expired yet.')

    @mock.patch('family_foto.models.auth_token.datetime')
    def test_token_expired(self, mock_datetime):
        """
        Test token is actually expired.
        """
        mock_datetime.utcnow = mock.Mock(return_value=datetime(1901, 12, 21))
        token = AuthToken.create_token(self.user, 100)
        mock_datetime.utcnow = mock.Mock(return_value=datetime(1901, 12, 21, 0, 1, 50))
        self.assertFalse(token.check(self.user.id))

    def test_wrong_id(self):
        """
        Test user is not owner of token.
        """
        other_user = add_user('other', 'user')
        token = AuthToken.create_token(other_user, 100)
        self.assertFalse(token.check(self.user.id))

    def test_revoke_token(self):
        """
        Tests if a token can be revoked.
        """
        token = AuthToken.create_token(self.user, 6000)
        token.revoke()
        self.assertFalse(token.check(self.user.id), msg=f'{token} is still valid.')
