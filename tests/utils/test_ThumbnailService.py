from family_foto.models.photo import Photo
from family_foto.utils.ThumbnailService import ThumbnailService
from tests.base_photo_test_case import BasePhotoTestCase


class TestThumbnailService(BasePhotoTestCase):
    def test_generate_from_photo(self):
        photo = Photo(filename='example.jpg', url='/photos/example.jpg')
        path = ThumbnailService.generate(photo)
        self.assertEqual('/resized-images/400_400_example.jpg', path)
