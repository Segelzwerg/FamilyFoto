import os
from io import BytesIO
from shutil import rmtree

from flask_api import status

from family_foto.models.photo import Photo
from family_foto.models.video import Video
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_video_test_case import VIDEOS_SAVE_PATH

PHOTOS_SAVE_PATH = './photos'


class UploadTestCase(BaseLoginTestCase):
    """
    Test case for uploading media files.
    """

    def setUp(self):
        super().setUp()
        if os.path.exists(PHOTOS_SAVE_PATH):
            rmtree(PHOTOS_SAVE_PATH)
        if os.path.exists(VIDEOS_SAVE_PATH):
            rmtree(VIDEOS_SAVE_PATH)

    def tearDown(self):
        if os.path.exists(PHOTOS_SAVE_PATH):
            rmtree(PHOTOS_SAVE_PATH)
        if os.path.exists(VIDEOS_SAVE_PATH):
            rmtree(VIDEOS_SAVE_PATH)
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

    def test_upload_video(self):
        """
        Tests if upload of a video works.
        """
        with self.client:
            with open('../data/example.mp4', 'rb') as file:
                data = dict(file=(file, 'example.mp4'))
                response = self.client.post('/upload',
                                            content_type='multipart/form-data',
                                            data=data)
                file.close()
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertIn('example.mp4', os.listdir(VIDEOS_SAVE_PATH))
            self.assertIn('example.mp4', [video.filename for video in Video.query.all()])
