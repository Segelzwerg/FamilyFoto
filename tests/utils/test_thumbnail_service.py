from unittest.mock import Mock, patch

import ffmpeg

from family_foto.utils.thumbnail_service import ThumbnailService
from tests.base_media_test_case import BaseMediaTestCase
from tests.test_utils.test_classes import UnsupportedFileType


class TestThumbnailService(BaseMediaTestCase):
    """
    Tests the thumbnail service.
    """

    def test_generate_from_photo(self):
        """
        Tests the thumbnail service for a photo.
        """
        path = ThumbnailService.generate(self.photo)
        self.assertEqual('/resized-images/400_400_example.jpg', path)

    def test_generate_from_video(self):
        """
        Tests the thumbnail service for a video.
        """
        path = ThumbnailService.generate(self.video)
        self.assertEqual('/resized-images/400_400_example.mp4.jpg', path)

    def test_generate_unsupported_type(self):
        """
        Tests if an error is raised for an unsupported type.
        """
        with self.assertRaises(TypeError):
            ThumbnailService.generate(UnsupportedFileType())

    def test_video_thumbnail_already_exists(self):
        """
        Tests if the thumbnail is no recreated.
        """
        _ = ThumbnailService.generate(self.video)
        with patch('family_foto.utils.image.resize') as resize:
            _ = ThumbnailService.generate(self.video)
            resize.assert_not_called()

    def test_photo_thumbnail_already_exists(self):
        """
        Tests if the thumbnail is no recreated.
        """
        _ = ThumbnailService.generate(self.photo)
        with patch('resizeimage.resizeimage.resize_width') as resize:
            _ = ThumbnailService.generate(self.photo)
            resize.assert_not_called()

    @patch('ffmpeg._ffmpeg.input', Mock(side_effect=ffmpeg.Error))
    def test_thumbnail_fail(self):
        """
        Tests a failure in creating a thumbnail raises an error.
        """
        with self.assertRaisesRegex(IOError, 'Could not read frames from'):
            self.video.thumbnail(200, 200)
