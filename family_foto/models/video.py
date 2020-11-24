import os
import random

import ffmpeg
from flask import current_app
from sqlalchemy import ForeignKey

from family_foto.const import UPLOADED_VIDEOS_DEST_RELATIVE, RESIZED_DEST
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
    def frame_count(self) -> int:
        streams: list[dict] = self.meta['streams']
        for stream in streams:
            if stream['codec_type'] == 'video':
                return int(stream['nb_frames'])

        raise RuntimeError('could not read length from video file')

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
        if not os.path.exists(current_app.config[RESIZED_DEST]):
            os.mkdir(current_app.config[RESIZED_DEST])
        path = f'{current_app.config[RESIZED_DEST]}/{width}_{height}_{self.filename}.png'

        frame = random.randint(0, self.frame_count)
        try:
            (ffmpeg.input(self.abs_path)
             .trim(start_frame=frame, end_frame=frame + 2)
             .output(path,
                     s=f'{width}x{height}',
                     frames='1')
             .run(capture_stdout=True,
                  capture_stderr=False))
        except ffmpeg.Error as e:
            raise IOError(f'Could not read frames from {path}', e)

        return path
