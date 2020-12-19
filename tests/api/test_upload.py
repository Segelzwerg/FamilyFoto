import os

from flask_api import status
from flask_login import current_user

from family_foto.models.file import File
from tests.base_login_test_case import BaseLoginTestCase


class ApiUploadTestCase(BaseLoginTestCase):
    """
    Tests the upload via API.
    """

    def setUp(self):
        super().setUp()
        self.video_filename = 'example.mp4'
        self.photo_filename = 'example.jpg'
        self.video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data',
                                       self.video_filename)
        self.photo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data',
                                       self.photo_filename)

        self.token = current_user.get_token()

    def test_upload_photo(self):
        """
        Test upload of a photo from API.
        """

        file = open(self.photo_path, 'rb')
        data = dict(files=[(file, self.photo_filename)])
        response = self.client.post('/api/upload',
                                    headers={'Authorization': f'Bearer {self.token.token}'},
                                    content_type='multipart/form-data',
                                    data=data)
        file.close()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(File.query.all()))

    def test_upload_video(self):
        """
        Test upload of a video from API.
        """
        file = open(self.video_path, 'rb')
        data = dict(files=[(file, self.video_filename)])
        response = self.client.post('/api/upload',
                                    headers={'Authorization': f'Bearer {self.token.token}'},
                                    content_type='multipart/form-data',
                                    data=data)
        file.close()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(File.query.all()))

    def test_upload_multiple(self):
        """
        Tests if a uploading multiple files at once works.
        """
        photo = open(self.photo_path, 'rb')
        video = open(self.video_path, 'rb')
        data = dict(files=[(photo, self.photo_filename), (video, self.video_filename)])
        response = self.client.post('/api/upload',
                                    headers={'Authorization': f'Bearer {self.token.token}'},
                                    content_type='multipart/form-data',
                                    data=data)
        photo.close()
        video.close()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(File.query.all()))
