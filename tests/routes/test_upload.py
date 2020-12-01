import os
from io import BytesIO

from flask_api import status

from family_foto.models.photo import Photo
from family_foto.models.video import Video
from tests.base_login_test_case import BaseLoginTestCase


class UploadTestCase(BaseLoginTestCase):
    """
    Test case for uploading media files.
    """

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
            self.assertIn('foto.jpg', os.listdir(self.app.config['UPLOADED_PHOTOS_DEST']))
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
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        if os.path.exists(self.app.config['UPLOADED_PHOTOS_DEST']):
            self.assertNotIn('foto.jpg', os.listdir(self.app.config['UPLOADED_PHOTOS_DEST']))

    def test_upload_video(self):
        """
        Tests if upload of a video works.
        """
        with self.client:
            data = dict(file=(BytesIO(b'my file contents'), 'example.mp4'))
            response = self.client.post('/upload',
                                        content_type='multipart/form-data',
                                        data=data)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertIn('example.mp4', os.listdir(self.app.config['UPLOADED_VIDEOS_DEST']))
            self.assertIn('example.mp4', [video.filename for video in Video.query.all()])
