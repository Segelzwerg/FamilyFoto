from family_foto.app import add_user
from family_foto.models.photo import Photo
from tests.base_test_case import BaseTestCase


class PhotoTestCase(BaseTestCase):
    """
    Tests the functionality of the Photo Entity.
    """

    def setUp(self):
        super().setUp()
        self.user = add_user('marcel', '123')
        self.other_user = add_user('lea', '654')
        self.photo = Photo(filename='test.jpg', user=self.user)

    def test_path(self):
        """
        Tests the path property.
        """
        filename = 'test.jpg'
        photo = Photo(filename=filename, url='/photos/test.jpg')
        self.assertEqual(f'./photos/{filename}', photo.path)

    def test_sharing_via_all(self):
        """
        Tests the permission via all sharing.
        """
        self.user.share_all_with(self.other_user)
        self.assertTrue(self.photo.has_read_permission(self.other_user),
                        msg=f'{self.other_user} has no general reading permission of {self.user}\'s'
                            f'photos.')

    def test_sharing_via_all_not_granted(self):
        """
        Tests the permission via all sharing which is not granted.
        """
        self.assertFalse(self.photo.has_read_permission(self.other_user),
                         msg=f'{self.other_user} has general reading permission of {self.user}\'s'
                             f'photos.')
