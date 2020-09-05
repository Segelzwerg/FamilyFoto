from io import BytesIO

from flask_api import status
from flask_login import current_user

from family_foto.app import add_user
from family_foto.models import db
from family_foto.models.photo import Photo
from tests.base_photo_test_case import BasePhotoTestCase
from tests.base_login_test_case import BaseLoginTestCase

PHOTOS_SAVE_PATH = './photos'


class GalleryTestCase(BaseLoginTestCase, BasePhotoTestCase):
    """
    Testcase for the gallery display.
    """

    def test_gallery_route(self):
        """
        Tests if the gallery route is working.
        """
        response = self.client.get('/gallery')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_all_photos_from_user(self):
        """
        Tests that gets all photos from an user.
        """
        file = dict(
            file=(BytesIO(b'my file contents'), "foto.jpg"),
        )
        self.client.post('/upload',
                         content_type='multipart/form-data',
                         data=file)
        photos = current_user.get_photos()
        all_photos = Photo.query.all()
        self.assertListEqual(photos, all_photos)

    def test_get_all_photos_from_user_but_not_from_others(self):
        """
        Tests that it does not get the others.
        """
        file = dict(
            file=(BytesIO(b'my file contents'), "foto.jpg"),
        )
        self.client.post('/upload',
                         content_type='multipart/form-data',
                         data=file)
        other_photo = Photo(filename='other-photo.jpg', user=2)
        db.session.add(other_photo)
        db.session.commit()
        photos = current_user.get_photos()
        all_photos = Photo.query.all()
        self.assertIn(other_photo, all_photos)
        self.assertNotIn(other_photo, photos)

    def test_show_shared(self):
        """
        Tests if an user can see photos that others shared with him/her/it.
        """
        other_user = add_user('sharer', 'sharing')
        other_photo = Photo(filename='other-photo.jpg', user=other_user.id)
        db.session.add(other_photo)
        db.session.commit()
        other_user.share_all_with(current_user)
        photos = current_user.get_photos()
        self.assertIn(other_photo, photos)

    def test_get_original_photo(self):
        """
        Tests if original photo can be retrieved.
        """
        file = dict(
            file=(BytesIO(b'my file contents'), "foto.jpg"),
        )
        self.client.post('/upload',
                         content_type='multipart/form-data',
                         data=file)
        response = self.client.get('/photo/foto.jpg')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
