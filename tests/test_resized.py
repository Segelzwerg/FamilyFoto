from flask_api import status

from tests.base_login_test_case import BaseLoginTestCase
from tests.base_photo_test_case import BasePhotoTestCase


class ResizedTestCase(BasePhotoTestCase, BaseLoginTestCase):
    """
    Tests the route for resizing images.
    """

    def test_route(self):
        """
        Tests the route is working.
        """
        response = self.client.get(f'/resized-images/{self.photo.filename}')
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response)
