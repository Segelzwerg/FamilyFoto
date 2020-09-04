import os
from shutil import copyfile, rmtree

import pytest
from werkzeug.datastructures import FileStorage

from family_foto.models.photo import Photo
from tests.base_test_case import BaseTestCase

PHOTOS_SAVE_PATH = './photos'


class PhotoTestCase(BaseTestCase):
    """
    Tests the functionality of the Photo Entity.
    """

    @pytest.fixture
    def example_image(self):
        file_path = 'data/example-image.jpg'
        file = open(file_path, 'rb')
        return FileStorage(stream=file, filename=file_path, content_type='image')

    def setUp(self):
        super(PhotoTestCase, self).setUp()
        if not os.path.exists('./photos'):
            os.mkdir(PHOTOS_SAVE_PATH)
        copyfile('./data/example.jpg', f'{PHOTOS_SAVE_PATH}/example.jpg')
        self.photo = Photo(filename='example.jpg', url='/photos/example.jpg')

    def tearDown(self):
        if os.path.exists(PHOTOS_SAVE_PATH):
            rmtree(PHOTOS_SAVE_PATH)
        super().tearDown()

    def test_path(self):
        """
        Tests the path property.
        """
        filename = 'test.jpg'
        photo = Photo(filename=filename, url='/photos/test.jpg')
        self.assertEqual(f'./photos/{filename}', photo.path)

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
