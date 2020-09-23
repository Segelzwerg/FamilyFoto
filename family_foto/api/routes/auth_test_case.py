import base64

from flask_api import status

from tests.base_login_test_case import BaseLoginTestCase


class ApiAuthRouteTestCase(BaseLoginTestCase):
    """
    Tests the api authentication routes.
    """

    def test_token_route(self):
        """
        Tests the route /api/token
        """
        with self.client:
            credentials = base64.b64encode(b'marcel:1234').decode('utf-8')
            response = self.client.post('api/token', headers={
                'Authorization': f'Basic {credentials}'})
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_token_route_wrong_password(self):
        """
        Tests the route /api/token with wrong password.
        """
        with self.client:
            credentials = base64.b64encode(b'marcel:123').decode('utf-8')
            response = self.client.post('api/token', headers={
                'Authorization': f'Basic {credentials}'})
            self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)