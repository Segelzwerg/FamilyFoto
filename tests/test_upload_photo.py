import os
from io import BytesIO
from shutil import rmtree
from unittest.mock import patch

from flask_api import status

from tests.base_test_case import BaseTestCase

PHOTOS_SAVE_PATH = './photos'


class PhotoUploadTestCase(BaseTestCase):
    """
    Test case for uploading photos.
    """

    def setUp(self):
        self.patcher = patch('flask_login.utils._get_user')
        self.mock_current_user = self.patcher.start()

    def tearDown(self):
        if os.path.exists(PHOTOS_SAVE_PATH):
            rmtree(PHOTOS_SAVE_PATH)
        self.patcher.stop()

    def test_upload(self):
        """
        Tests if a jpg can be uploaded.
        """
        file = dict(
            file=(BytesIO(b'my file contents'), "foto.jpg"),
        )
        response = self.client.post('/upload',
                                    content_type='multipart/form-data',
                                    data=file)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('foto.jpg', os.listdir(PHOTOS_SAVE_PATH))

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
