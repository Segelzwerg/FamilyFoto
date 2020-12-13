import hashlib
import os
from shutil import rmtree, copyfile

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

        with open(path, 'rb') as file:
            file_hash = hashlib.sha3_256(bytes(file.read())).hexdigest()
            directory = f'{self.app.config["UPLOADED_PHOTOS_DEST"]}/{file_hash[:2]}/{file_hash}'
            os.makedirs(directory)
            copied_path = copyfile(path, directory + "/example.jpg")
            if not os.path.exists(copied_path):
                raise FileNotFoundError(f'{copied_path} does not exists.')
            self.photo = Photo(filename='example.jpg', hash=file_hash)
