from family_foto.models.photo import Photo
from family_foto.models.video import Video
from family_foto.utils.thumbnail_service import ThumbnailService
from tests.base_photo_test_case import BasePhotoTestCase
from tests.base_video_test_case import BaseVideoTestCase


class TestThumbnailService(BasePhotoTestCase, BaseVideoTestCase):
    """
    Tests the thumbnail service.
    """
    def test_generate_from_photo(self):
        """
        Tests the thumbnail service for a photo.
        """
        photo = Photo(filename='example.jpg', url='/photos/example.jpg')
        path = ThumbnailService.generate(photo)
        self.assertEqual('/resized-images/400_400_example.jpg', path)

    def test_generate_from_video(self):
        """
        Tests the thumbnail service for a video.
        """
        video = Video(filename='example.mp4', url='/videos/example.mp4')
        path = ThumbnailService.generate(video)
        self.assertEqual('/resized-images/400_400_example.mp4.jpg', path)
