from datetime import datetime

import ffmpeg
from flask import current_app
from sqlalchemy import ForeignKey

from family_foto.const import UPLOADED_VIDEOS_DEST_RELATIVE
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
    def creation_datetime(self):
        """
        :return: a datetime object of creation date.
        """
        creation_time = self.meta['format']['tags']['creation_time'].split('.')[0]
        return datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%S')

    @property
    def year(self):
        """
        :return: year of creation
        """
        return self.creation_datetime.year

    @property
    def month(self):
        """
        :return: month of creation
        """
        return self.creation_datetime.month

    @property
    def day(self):
        """
        :return: day of creation
        """
        return self.creation_datetime.day

    @property
    def frame_count(self) -> int:
        """
        Returns the frame count of the video.
        """
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
        sub_path = f'{self.get_hash[:2]}/{self.get_hash}/{self.filename}'
        return f'{current_app.config[UPLOADED_VIDEOS_DEST_RELATIVE]}/{sub_path}'
