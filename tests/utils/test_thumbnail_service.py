from pytest import raises

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
        with raises(TypeError):
            ThumbnailService.generate(UnsupportedFileType())
