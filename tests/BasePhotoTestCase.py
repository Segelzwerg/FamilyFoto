import os
from shutil import rmtree, copyfile

from family_foto.models.photo import Photo
from tests.base_test_case import BaseTestCase

PHOTOS_SAVE_PATH = './photos'
RESIZED_SAVE_PATH = './resized-images'


class BasePhotoTestCase(BaseTestCase):
    def setUp(self):
        super(BasePhotoTestCase, self).setUp()
        if not os.path.exists('./photos'):
            os.mkdir(PHOTOS_SAVE_PATH)
        if os.path.exists(RESIZED_SAVE_PATH):
            rmtree(RESIZED_SAVE_PATH)
        Photo.query.delete()

        copied_path = copyfile('./data/example.jpg', f'{PHOTOS_SAVE_PATH}/example.jpg')
        if not os.path.exists(copied_path):
            raise FileNotFoundError(f'{copied_path} does not exists.')
        self.photo = Photo(filename='example.jpg', url='/photos/example.jpg')

    def tearDown(self):
        if os.path.exists(PHOTOS_SAVE_PATH):
            rmtree(PHOTOS_SAVE_PATH)
        super().tearDown()
