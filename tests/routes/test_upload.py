import os
from io import BytesIO

from flask_api import status

from family_foto import File
from family_foto.models.photo import Photo
from family_foto.models.video import Video
from tests.base_login_test_case import BaseLoginTestCase
from tests.test_utils.tasks import upload_test_file


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
            path = self.app.config['UPLOADED_PHOTOS_DEST']
            dir_content = os.listdir(path)
            path = path + '/' + dir_content[0]
            dir_content = os.listdir(path)
            dir_content = os.listdir(path + '/' + dir_content[0])

            self.assertIn('foto.jpg', dir_content)
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

            path = self.app.config['UPLOADED_VIDEOS_DEST']
            dir_content = os.listdir(path)
            path = path + '/' + dir_content[0]
            dir_content = os.listdir(path)
            dir_content = os.listdir(path + '/' + dir_content[0])

            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertIn('example.mp4', dir_content)
            self.assertIn('example.mp4', [video.filename for video in Video.query.all()])

    def test_duplication_upload(self):
        """
        Tests if a file can not be uploaded twice.
        """
        with self.client:
            filename = 'test.jpg'
            upload_test_file(self.client, filename)
            upload_test_file(self.client, filename)
            file = File.query.filter_by(filename=filename).first()
            files = File.query.filter_by(filename=filename).all()

            self.assertEqual([file], files)

    def test_upload_same_name_different_file(self):
        """
        Tests if a file with same name but different content can be uploaded.
        """
        filename = 'test.jpg'
        upload_test_file(self.client, filename)
        upload_test_file(self.client, filename, 'example_1.jpg')
        files = File.query.all()
        self.assertEqual(2, len(files))

    def test_upload_multiple(self):
        """
        Tests if a uploading multiple files at once works.
        """
        photo_filename = 'example.jpg'
        video_filename = 'example.mp4'
        photo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data',
                                  photo_filename)
        video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data',
                                  video_filename)
        photo = open(photo_path, 'rb')
        video = open(video_path, 'rb')
        data = dict(file=[(photo, photo_filename), (video, video_filename)])
        self.client.post('/upload',
                         content_type='multipart/form-data',
                         data=data)
        photo.close()
        video.close()
        files = File.query.all()
        self.assertEqual(2, len(files))
