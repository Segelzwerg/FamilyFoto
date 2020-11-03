import os
from shutil import rmtree

from PIL import Image

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
        expected_path = 'videos/example.mp4'
        self.assertEqual(expected_path, self.video.path)

    def test_thumbnail_video(self):
        """
        Tests the rendering of the thumbnail of the video.
        """
        path = self.video.thumbnail(200, 200)
        image = Image.open(path)
        self.assertTrue(os.path.isfile(path), msg=f'{path} does not exist.')
        self.assertEqual(200, image.width)

    def test_thumbnail_dir_not_exists(self):
        """
        Tests the creation of thumbnail if the thumbnail directory does not exist.
        """
        if os.path.exists(self.app.config['RESIZED_DEST']):
            rmtree(self.app.config['RESIZED_DEST'])
        path = self.video.thumbnail(200, 200)
        image = Image.open(path)
        self.assertTrue(os.path.exists(path), msg=f'{path} does not exist.')
        self.assertEqual(200, image.width)

    def test_video_url(self):
        """
        Tests the return value of the url property.
        """
        self.assertEqual('/videos/example.mp4', self.video.url)
