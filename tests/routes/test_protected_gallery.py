from flask_api import status

from tests.base_login_test_case import BaseLoginTestCase


class ProtectedGalleryTestCase(BaseLoginTestCase):
    def test_route(self):
        response = self.client.get('/public')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
