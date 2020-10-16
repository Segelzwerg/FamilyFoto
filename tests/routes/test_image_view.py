from flask_api import status

from family_foto.models import db
from family_foto.models.photo import Photo
from family_foto.web import add_user
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_photo_test_case import BasePhotoTestCase


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

    def test_shared_individual_photo(self):
        """
        Tests sharing an individual photo with another user.
        """
        db.session.add(self.photo)
        db.session.commit()
        other_user = add_user('other', 'user')
        response = self.client.post('/image/example.jpg', data=dict(share_with=[other_user.id]))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
