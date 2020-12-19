import hashlib
import os
from shutil import copyfile

from family_foto.models.file import File
from family_foto.models.video import Video
from tests.base_test_case import BaseTestCase


class BaseVideoTestCase(BaseTestCase):
    """
    Base Setup for usage of videos.
    """

    def setUp(self):
        super().setUp()
        if not os.path.exists(self.app.config['UPLOADED_VIDEOS_DEST']):
            os.mkdir(self.app.config['UPLOADED_VIDEOS_DEST'])
        File.query.delete()
        Video.query.delete()

        filename = 'example.mp4'
        path = os.path.join(os.path.dirname(__file__), f'data/{filename}')
        with open(path, 'rb') as file:
            file_hash = hashlib.sha3_256(bytes(file.read())).hexdigest()
            directory = f'{self.app.config["UPLOADED_VIDEOS_DEST"]}/{file_hash[:2]}/{file_hash}'
            os.makedirs(directory)
            copied_path = copyfile(path, directory + f'/{filename}')
            if not os.path.exists(copied_path):
                raise FileNotFoundError(f'{copied_path} does not exists.')
            self.video = Video(filename=filename, hash=file_hash)
