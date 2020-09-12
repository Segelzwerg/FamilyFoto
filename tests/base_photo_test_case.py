import os
from shutil import rmtree, copyfile

from family_foto.models import db
from family_foto.models.file import File
from family_foto.models.photo import Photo
from tests.base_test_case import BaseTestCase

PHOTOS_SAVE_PATH = './photos'
RESIZED_SAVE_PATH = './resized-images'


class BasePhotoTestCase(BaseTestCase):
    """
    Base Test Case with handles everything regarding photos.
    """

    def setUp(self):
        super().setUp()
        if not os.path.exists('./photos'):
            os.mkdir(PHOTOS_SAVE_PATH)
        if os.path.exists(RESIZED_SAVE_PATH):
            rmtree(RESIZED_SAVE_PATH)
        File.query.delete()
        Photo.query.delete()

        copied_path = copyfile('./data/example.jpg', f'{PHOTOS_SAVE_PATH}/example.jpg')
        if not os.path.exists(copied_path):
            raise FileNotFoundError(f'{copied_path} does not exists.')
        self.photo = Photo(filename='example.jpg', url='/photos/example.jpg')

    def tearDown(self):
        if os.path.exists(PHOTOS_SAVE_PATH):
            rmtree(PHOTOS_SAVE_PATH)
        super().tearDown()

    def test_commit(self):
        """Tests committing the file works"""
        db.session.add(self.photo)
        db.session.commit()

        photo = Photo.query.get(self.photo.id)
        self.assertEqual(self.photo, photo)
