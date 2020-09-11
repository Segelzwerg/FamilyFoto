import os
import random

import cv2
import ffmpeg
from sqlalchemy import ForeignKey

from family_foto.config import BaseConfig
from family_foto.models import db
from family_foto.models.file import File


class Video(File):
    """
    Class of the video entity.
    """
    id = db.Column(db.Integer, ForeignKey('file.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'video'
    }

    @property
    def meta(self):
        """
        Returns the meta data of the video.
        """
        return ffmpeg.probe(self.path)

    @property
    def path(self):
        """
        Returns path to video file.
        """
        return f'{BaseConfig.UPLOADED_VIDEOS_DEST}/{self.filename}'

    def thumbnail(self, width: int, height: int):
        """
        Returns a still frame with play logo on top.
        :param width: thumbnail width in pixel
        :param height: thumbnail height in pixel (aspect ratio will be kept)
        """
        video = cv2.VideoCapture(self.path)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

        video.set(cv2.CAP_PROP_POS_FRAMES, random.randint(0, frame_count))
        ret, frame = video.read()
        path = f'{BaseConfig.RESIZED_DEST}/{width}_{height}_{self.filename}.jpg'
        if not os.path.exists(BaseConfig.RESIZED_DEST):
            os.mkdir(BaseConfig.RESIZED_DEST)
        if not cv2.imwrite(path, frame):
            raise IOError(f'could not write {path}')
        video.release()
        cv2.destroyAllWindows()
        return path.lstrip('.')
