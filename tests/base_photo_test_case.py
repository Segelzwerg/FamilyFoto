import os
from shutil import rmtree, copyfile

from family_foto.models import db
from family_foto.models.file import File
from family_foto.models.photo import Photo
from tests.base_test_case import BaseTestCase


class BasePhotoTestCase(BaseTestCase):
    """
    Base Test Case with handles everything regarding photos.
    """

    def setUp(self):
        super().setUp()
        if not os.path.exists(self.app.config['UPLOADED_PHOTOS_DEST']):
            os.mkdir(self.app.config['UPLOADED_PHOTOS_DEST'])
        if os.path.exists(self.app.config['RESIZED_DEST']):
            rmtree(self.app.config['RESIZED_DEST'])
        File.query.delete()
        Photo.query.delete()

        path = os.path.join(os.path.dirname(__file__), 'data/example.jpg')
        copied_path = copyfile(path, f'{self.app.config["UPLOADED_PHOTOS_DEST"]}/example.jpg')
        if not os.path.exists(copied_path):
            raise FileNotFoundError(f'{copied_path} does not exists.')
        self.photo = Photo(filename='example.jpg', url='/photos/example.jpg')

    def test_commit(self):
        """Tests committing the file works"""
        db.session.add(self.photo)
        db.session.commit()

        photo = Photo.query.get(self.photo.id)
        self.assertEqual(self.photo, photo)
