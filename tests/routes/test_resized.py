from flask_api import status

from family_foto.models import db
from family_foto.services.thumbnail_service import generate
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
        length = 200
        self.photo.user = self.mock_current_user.id
        db.session.add(self.photo)
        db.session.commit()
        generate(self.photo, length, length)
        response = self.client.get(self.photo.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response)
