import os

from tests.base_video_test_case import VideoBaseTestCase


class VideoTestCase(VideoBaseTestCase):
    """
    Test the functionality of the video entity.
    """

    def setUp(self):
        super().setUp()

    def test_thumbnail_video(self):
        """
        Tests the rendering of the thumbnail of the video.
        """
        path = self.video.thumbnail(200, 200)
        self.assertTrue(os.path.exists(path), msg=f'{path} does not exists.')
