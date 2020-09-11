import os
from io import BytesIO
from shutil import rmtree

from flask_api import status

from family_foto.models.photo import Photo
from tests.base_login_test_case import BaseLoginTestCase

PHOTOS_SAVE_PATH = './photos'


class UploadTestCase(BaseLoginTestCase):
    """
    Test case for uploading photos.
    """

    def tearDown(self):
        if os.path.exists(PHOTOS_SAVE_PATH):
            rmtree(PHOTOS_SAVE_PATH)
        super().tearDown()

    def test_upload(self):
        """
        Tests if a jpg can be uploaded.
        """
        with self.client:
            file = dict(
                file=(BytesIO(b'my file contents'), "foto.jpg"),
            )
            response = self.client.post('/upload',
                                        content_type='multipart/form-data',
                                        data=file)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertIn('foto.jpg', os.listdir(PHOTOS_SAVE_PATH))
            self.assertIn('foto.jpg', [photo.filename for photo in Photo.query.all()])

    def test_upload_wrong_file_type(self):
        """
        Tests if a doc upload fails.
        """
        file = dict(
            file=(BytesIO(b'my file contents'), "foto.doc"),
        )
        response = self.client.post('/upload',
                                    content_type='multipart/form-data',
                                    data=file)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        if os.path.exists(PHOTOS_SAVE_PATH):
            self.assertNotIn('foto.jpg', os.listdir(PHOTOS_SAVE_PATH))
