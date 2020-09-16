from base64 import b64encode

from flask_api import status

from tests.base_login_test_case import BaseLoginTestCase


class ApiAuthTestCase(BaseLoginTestCase):
    def test_token_getter(self):
        """
        Tests the api route for getting a token.
        """
        with self.client:
            credentials = b64encode(b'marcel:1234').decode('utf-8')
            response = self.client.post('/api/token',
                                        headers={'Authorization': f'Basic {credentials}'})

            self.assertEqual(status.HTTP_200_OK, response.status_code)
