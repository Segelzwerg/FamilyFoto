from unittest.mock import Mock, patch

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

    @patch('family_foto.utils.image.get_random_frame', Mock(return_value=None))
    def test_generate_cv2_error(self):
        """
        Tests if the an error is raised if a frame could not be extracted.
        """
        with self.assertRaisesRegex(IOError, 'Could not read video:'):
            ThumbnailService.generate(self.video)

    def test_video_thumbnail_already_exists(self):
        """
        Tests if the thumbnail is no recreated.
        """
        _ = ThumbnailService.generate(self.video)
        with patch('family_foto.utils.image.resize') as resize:
            _ = ThumbnailService.generate(self.video)
            resize.assert_not_called()
