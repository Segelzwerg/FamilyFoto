import os
from io import BytesIO
from shutil import rmtree
from unittest.mock import patch

from flask_api import status
from flask_login import current_user

from family_foto.models import db
from family_foto.models.photo import Photo
from family_foto.models.user import User
from tests.base_test_case import BaseTestCase

PHOTOS_SAVE_PATH = './photos'


class GalleryTestCase(BaseTestCase):
    """
    Testcase for the gallery display.
    """
    def setUp(self):
        super().setUp()
        self.patcher = patch('flask_login.utils._get_user')
        self.mock_current_user = self.patcher.start()
        self.mock_current_user.return_value = User(id=1,
                                                   username='marcel')

    def tearDown(self):
        if os.path.exists(PHOTOS_SAVE_PATH):
            rmtree(PHOTOS_SAVE_PATH)
        self.patcher.stop()
        super().tearDown()

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

    def test_get_original_photo(self):
        file = dict(
            file=(BytesIO(b'my file contents'), "foto.jpg"),
        )
        self.client.post('/upload',
                         content_type='multipart/form-data',
                         data=file)
        response = self.client.get('/photo/foto.jpg')
        self.assertEqual(status.HTTP_200_OK, response.status_code)