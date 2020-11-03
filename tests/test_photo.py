import os

from family_foto import add_user
from family_foto.models.photo import Photo
from tests.base_photo_test_case import BasePhotoTestCase


class PhotoTestCase(BasePhotoTestCase):
    """
    Tests the functionality of the Photo Entity.
    """

    def setUp(self):
        super().setUp()
        self.user = add_user('marcel', '123')
        self.other_user = add_user('lea', '654')
        self.photo.user = self.user.id

    def test_path(self):
        """
        Tests the path property.
        """
        filename = 'test.jpg'
        photo = Photo(filename=filename, url='/photos/test.jpg')
        self.assertEqual(f'photos/{filename}', photo.path)

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

    def test_sharing_via_individual(self):
        """
        Tests sharing for an individual photo.
        """
        self.photo.share_with(self.other_user)
        self.assertTrue(self.photo.has_read_permission(self.other_user),
                        msg=f'{self.other_user} has no permission for this photo by {self.user}.')

    def test_sharing_via_individual_multiple(self):
        """
        Tests sharing for an individual photo with multiple users.
        """
        third_user = add_user('third', '3')
        self.photo.share_with([self.other_user, third_user])
        self.assertTrue(self.photo.has_read_permission(self.other_user),
                        msg=f'{self.other_user} has no permission for this photo by {self.user}.')
        self.assertTrue(self.photo.has_read_permission(third_user),
                        msg=f'{third_user} has no permission for this photo by {self.user}.')

    def test_sharing_via_individual_not_granted(self):
        """
        Tests sharing for an individual photo is not granted.
        """
        self.assertFalse(self.photo.has_read_permission(self.other_user),
                         msg=f'{self.other_user} has permission for this photo by {self.user}.')

    def test_meta(self):
        """
        Test the meta data property.
        """
        expected_dict = dict(DateTime='2020:08:18 12:44:08',
                             ExifImageWidth='4208',
                             ExifImageHeight='3120',
                             Flash='0',
                             FNumber='2.2',
                             FocalLength='3.5',
                             ISOSpeedRatings='113',
                             Make='BullittGroupLimited',
                             Model='S41')
        test_status, test_message = self._test_meta(expected_dict, self.photo.meta)
        self.assertTrue(test_status, msg=test_message)

    def test_height(self):
        """
        Tests the height property.
        """
        height = self.photo.height
        self.assertEqual(3120, height)

    def test_width(self):
        """
        Tests the width property.
        """
        width = self.photo.width
        self.assertEqual(4208, width)

    def test_resize(self):
        """
        Tests if photos are correctly resized.
        """
        resized_path = self.photo.thumbnail(400, 400)
        self.assertTrue(os.path.isfile(resized_path), msg=f'{resized_path} does not exist.')

    def test_image_view_path(self):
        """
        Tests the image view path.
        """
        self.assertEqual(f'/image/{self.photo.filename}', self.photo.image_view)

    @staticmethod
    def _test_meta(expected_dict, meta):
        keys_not_in = {k: v for k, v in expected_dict.items() if k not in meta.keys()}
        msg = f'photo.meta does not contain following keys:{keys_not_in}' if len(
            keys_not_in) > 0 else ''
        different_values = {}
        for key, val1 in expected_dict.items():
            val2 = meta.get(key)
            if val2 is not None and val1 != val2:
                different_values[key] = f'{val1, val2}'
        msg = msg + f'\nfollowing values are different {different_values}'
        if len(different_values) == 0 and len(keys_not_in) == 0:
            return True, msg
        return False, msg
