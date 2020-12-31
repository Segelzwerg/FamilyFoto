from io import BytesIO

from flask_api import status
from flask_login import current_user

from family_foto.models import db
from family_foto.models.file import File
from family_foto.models.photo import Photo
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_photo_test_case import BasePhotoTestCase
from tests.test_utils.assertions import assertImageIsLoaded
from tests.test_utils.tasks import upload_test_file


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
        upload_test_file(self.client)
        photos = current_user.get_media()
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
        photos = current_user.get_media()
        all_photos = Photo.query.all()
        self.assertIn(other_photo, all_photos)
        self.assertNotIn(other_photo, photos)

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
        photo: Photo = Photo.query.filter_by(filename='foto.jpg').first()
        response = self.client.get(photo.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_image_is_displayed(self):
        """
        Tests the images in the gallery are displayed.
        """
        filename = 'test.jpg'
        upload_test_file(self.client, filename)
        file = File.query.filter_by(filename=filename).first()
        response = self.client.get(f'/image/{file.hash}')
        assertImageIsLoaded(self, response)
