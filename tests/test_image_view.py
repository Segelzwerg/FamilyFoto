from family_foto.models import db
from tests.BasePhotoTestCase import BasePhotoTestCase
from tests.base_login_test_case import BaseLoginTestCase


class ImageViewTestCase(BaseLoginTestCase, BasePhotoTestCase):
    """
    Tests the image route.
    """

    def test_route(self):
        """
        Tests if the route works for an example image.
        """
        db.session.add(self.photo)
        db.session.commit()
        self.client.get('/image/example.jpg')

    def test_only_show_allowed_photos(self):
        """
        Tests if the user can only see photos he/she/it has permission to view.
        """
        pass