import os

from PIL import Image
from flask import current_app

from family_foto.models.video import Video
from family_foto.services.thumbnail_service import generate
from tests.base_video_test_case import BaseVideoTestCase


class VideoTestCase(BaseVideoTestCase):
    """
    Test the functionality of the video entity.
    """

    def setUp(self):
        super().setUp()
        link = 'https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1920_18MG.mp4'
        print(f'example video from: {link}')

    def test_path(self):
        """
        Tests the path property.
        """
        filename = 'test.mp4'
        video = Video(filename=filename, hash='abcd')
        self.assertEqual(f'videos/ab/abcd/{filename}', video.path)

    def test_thumbnail_video(self):
        """
        Tests the rendering of the thumbnail of the video.
        """
        path = generate(self.video, 200, 200)
        path = os.path.join(os.path.dirname(current_app.config['UPLOADED_VIDEOS_DEST']),
                            path.lstrip('/'))
        image = Image.open(path)
        self.assertTrue(os.path.isfile(path), msg=f'{path} does not exist.')
        self.assertEqual(200, image.width)

    def test_video_url(self):
        """
        Tests the return value of the url property.
        """
        filename = 'example.mp4'
        file_hash = 'abcd'
        url = f'/videos/{file_hash[:2]}/{file_hash}/{filename}'
        video = Video(filename=filename, hash=file_hash)
        self.assertEqual(url, video.url)

    def test_video_height(self):
        """
        Tests the video height property.
        """
        self.assertEqual(1080, self.video.height)

    def test_video_width(self):
        """
        Tests the video height property.
        """
        self.assertEqual(1920, self.video.width)

    def test_image_year(self):
        """
        Tests the year of creation.
        """
        self.assertEqual(self.video.year, 2015)

    def test_image_month(self):
        """
        Tests the month of creation.
        """
        self.assertEqual(self.video.month, 8)

    def test_image_day(self):
        """
        Tests the day of creation.
        """
        self.assertEqual(self.video.day, 7)

    def test_video_frame_count(self):
        """
        Tests the frame count property.
        """
        self.assertEqual(901, self.video.frame_count)

    def test_image_view_property(self):
        """
        Tests if the route is returned correctly.
        """
        self.assertEqual(f'/image/{self.video.hash}', self.video.image_view)
