from flask_api import status

from family_foto.app import add_user
from family_foto.models import db
from family_foto.models.photo import Photo
from tests.BasePhotoTestCase import BasePhotoTestCase
from tests.base_login_test_case import BaseLoginTestCase


class ImageViewTestCase(BaseLoginTestCase, BasePhotoTestCase):
    """
    Tests the image route.
    """

    def setUp(self):
        super().setUp()
        self.photo.user = self.mock_current_user.id

    def test_route(self):
        """
        Tests if the route works for an example image.
        """
        db.session.add(self.photo)
        db.session.commit()
        response = self.client.get('/image/example.jpg')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_only_show_allowed_photos(self):
        """
        Tests if the user can only see photos he/she/it has permission to view.
        """
        owner = add_user('owner', '123')
        other_photo = Photo(filename='example.jpg', url='/photos/example.jpg',
                            user=owner.id)
        db.session.add(other_photo)
        db.session.commit()
        response = self.client.get('/image/example.jpg')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
