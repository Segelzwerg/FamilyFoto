from flask_api import status

from family_foto import add_user, Role
from family_foto.models import db
from family_foto.models.photo import Photo
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_photo_test_case import BasePhotoTestCase
from tests.test_utils.assertions import assertImageIsLoaded, assertPublicSharing


class ImageViewTestCase(BaseLoginTestCase, BasePhotoTestCase):
    """
    Tests the image route.
    """

    def setUp(self):
        super().setUp()
        self.photo.user = self.mock_current_user.id
        self.user_role = Role.query.filter_by(name='user').first()
        db.session.add(self.photo)
        db.session.commit()

    def test_route(self):
        """
        Tests if the route works for an example image.
        """

        response = self.client.get(f'/image/{self.photo.hash}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_only_show_allowed_photos(self):
        """
        Tests if the user can only see photos he/she/it has permission to view.
        """
        owner = add_user('owner', '123', [self.user_role])
        other_photo = Photo(filename='example.jpg', user=owner.id, hash='zzzz')
        db.session.add(other_photo)
        db.session.commit()
        response = self.client.get(f'/image/{other_photo.hash}')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_shared_individual_photo(self):
        """
        Tests sharing an individual photo with another user.
        """
        other_user = add_user('other', 'user', [self.user_role])
        response = self.client.post(f'/image/{self.photo.hash}',
                                    data=dict(share_with=[other_user.id]))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_image_is_displayed(self):
        """
        Tests the images in the gallery are displayed.
        """
        response = self.client.get(f'/image/{self.photo.hash}')
        assertImageIsLoaded(self, response)

    def test_make_public(self):
        """
        Tests if a photo is set public.
        """
        self.photo.protected = False
        db.session.add(self.photo)
        _ = self.client.post(f'/image/{self.photo.hash}', data=dict(public='y'))
        self.assertEqual(True, self.photo.protected)

    def test_default_is_not_public(self):
        """
        Tests if the marker is not set on default.
        """
        self.photo.protected = False
        db.session.add(self.photo)
        db.session.commit()
        assertPublicSharing(self, value='n')

    def test_reset_public_status(self):
        """
        Tests the public access can be revoked.
        """
        _ = self.client.post(f'/image/{self.photo.hash}', data=dict(public='n'))
        assertPublicSharing(self, value='n')

    def test_authorized_access(self):
        """
        Tests if unauthorized access is denied.
        """
        owner = add_user('owner', '123', [self.user_role])
        photo = Photo(filename='other_file.mp4', hash='zzzz', user=owner.id)
        db.session.add(photo)
        db.session.commit()
        response = self.client.get(photo.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
