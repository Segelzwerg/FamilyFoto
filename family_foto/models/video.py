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
