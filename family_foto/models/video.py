import os
import random

import cv2
import ffmpeg
from flask import current_app
from sqlalchemy import ForeignKey

from family_foto import UPLOADED_VIDEOS_DEST_RELATIVE, RESIZED_DEST
from family_foto.models import db
from family_foto.models.file import File
from family_foto.utils.image import resize


class Video(File):
    """
    Class of the video entity.
    """

    id = db.Column(db.Integer, ForeignKey('file.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'video'
    }

    @property
    def image_view(self):
        return f'/image/{self.filename}'

    @property
    def height(self) -> int:
        streams: list[dict] = self.meta['streams']
        for stream in streams:
            if stream['codec_type'] == 'video':
                return int(stream['height'])

        raise RuntimeError('could not read height from video file')

    @property
    def width(self) -> int:
        streams: list[dict] = self.meta['streams']
        for stream in streams:
            if stream['codec_type'] == 'video':
                return int(stream['width'])

        raise RuntimeError('could not read width from video file')

    @property
    def meta(self):
        """
        Returns the meta data of the video.
        """
        return ffmpeg.probe(self.abs_path)

    @property
    def path(self):
        """
        Returns path to video file.
        """
        return current_app.config[UPLOADED_VIDEOS_DEST_RELATIVE] + "/" + self.filename

    def thumbnail(self, width: int, height: int):
        """
        Returns a still frame with play logo on top.
        :param width: thumbnail width in pixel
        :param height: thumbnail height in pixel (aspect ratio will be kept)
        """
        video = cv2.VideoCapture(self.abs_path)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

        video.set(cv2.CAP_PROP_POS_FRAMES, random.randint(0, frame_count))
        _, frame = video.read()

        path = f'{current_app.config[RESIZED_DEST]}/{width}_{height}_{self.filename}.jpg'
        if not os.path.exists(current_app.config[RESIZED_DEST]):
            os.mkdir(current_app.config[RESIZED_DEST])
        if not cv2.imwrite(path, frame):
            raise IOError(f'could not write {path}')
        path = resize(path, self.filename, width, height)
        video.release()
        cv2.destroyAllWindows()
        return path
