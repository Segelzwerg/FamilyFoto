from flask_api import status

from tests.base_login_test_case import BaseLoginTestCase


class ProtectedGalleryTestCase(BaseLoginTestCase):
    def test_route(self):
        response = self.client.get('/public')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_unauthorized_access(self):
        """
        Tests if a anonymous user will be redirected.
        """
        self.patcher.stop()
        response = self.client.get('/public')
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
