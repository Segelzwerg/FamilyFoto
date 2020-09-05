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
        copyfile('./data/example.jpg', f'{PHOTOS_SAVE_PATH}/example.jpg')
        self.photo = Photo(filename='example.jpg', url='/photos/example.jpg')
        Photo.query.delete()

    def tearDown(self):
        if os.path.exists(PHOTOS_SAVE_PATH):
            rmtree(PHOTOS_SAVE_PATH)
        super().tearDown()
