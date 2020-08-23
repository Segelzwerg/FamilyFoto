from family_foto.models.photo import Photo
from tests.base_test_case import BaseTestCase


class PhotoTestCase(BaseTestCase):
    """
    Tests the functionality of the Photo Entity.
    """
    def test_path(self):
        """
        Tests the path property.
        """
        filename = 'test.jpg'
        photo = Photo(filename=filename, url='/photos/test.jpg')
        self.assertEqual(f'./photos/{filename}', photo.path)
