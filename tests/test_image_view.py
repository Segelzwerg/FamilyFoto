from family_foto.models import db
from tests.BasePhotoTestCase import BasePhotoTestCase
from tests.base_login_test_case import BaseLoginTestCase


class ImageViewTestCase(BaseLoginTestCase, BasePhotoTestCase):
    """
    Tests the image route.
    """

    def test_route(self):
        db.session.add(self.photo)
        db.session.commit()
        self.client.get('/image/example.jpg')
