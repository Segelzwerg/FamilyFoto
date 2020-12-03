from flask_api import status

from family_foto import add_user, Role
from family_foto.models import db
from family_foto.models.photo import Photo
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_photo_test_case import BasePhotoTestCase
from tests.test_utils.assertions import assertImageIsLoaded
from tests.test_utils.tasks import upload_test_file


class ImageViewTestCase(BaseLoginTestCase, BasePhotoTestCase):
    """
    Tests the image route.
    """

    def setUp(self):
        super().setUp()
        self.photo.user = self.mock_current_user.id
        self.user_role = Role.query.filter_by(name='user').first()

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
        owner = add_user('owner', '123', [self.user_role])
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
        other_user = add_user('other', 'user', [self.user_role])
        response = self.client.post('/image/example.jpg', data=dict(share_with=[other_user.id]))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_image_is_displayed(self):
        """
        Tests the images in the gallery are displayed.
        """
        filename = 'test.jpg'
        upload_test_file(self.client)
        response = self.client.get(f'/image/{filename}')
        assertImageIsLoaded(self, response)

    def test_make_public(self):
        """
        Tests if a photo is set public.
        """
        self.photo.protected = False
        db.session.add(self.photo)
        _ = self.client.post(f'/image/{self.photo.filename}', data=dict(public='y'))
        self.assertEqual(True, self.photo.protected)
