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
        if not os.path.exists(self.app.config['RESIZED_DEST']):
            os.mkdir(self.app.config['RESIZED_DEST'])
        File.query.delete()
        Video.query.delete()

        path = os.path.join(os.path.dirname(__file__), 'data/example.mp4')
        copied_path = copyfile(os.path.abspath(path),
                               f'{self.app.config["UPLOADED_VIDEOS_DEST"]}/example.mp4')
        if not os.path.exists(copied_path):
            raise FileNotFoundError(f'{copied_path} does not exists.')
        self.video = Video(filename='example.mp4', url='/videos/example.mp4')
