from datetime import datetime

from PIL import Image, ExifTags
from flask import current_app
from sqlalchemy import ForeignKey

from family_foto.const import UPLOADED_PHOTOS_DEST_RELATIVE
from family_foto.logger import log
from family_foto.models import db
from family_foto.models.file import File


class Photo(File):
    """
    Class of Photo Entity
    """

    id = db.Column(db.Integer, ForeignKey('file.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'photo'
    }

    def __open_image(self) -> Image.Image:
        return Image.open(self.abs_path)

    @property
    def height(self):
        with self.__open_image() as image:
            return image.height
        # return int(self.meta['ExifImageHeight'])

    @property
    def width(self):
        with self.__open_image() as image:
            return image.width
        # return int(self.meta['ExifImageWidth'])

    @property
    def creation_datetime(self):
        """
        :return: a datetime object of creation date.
        """
        if len(self.meta) > 0:
            try:
                return datetime.strptime(self.meta['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
            except KeyError:
                log.warning(f'For {self.filename} there was no meta key: DateTimeOriginal')
            try:
                return datetime.strptime(self.meta['DateTime'], '%Y:%m:%d %H:%M:%S')
            except KeyError:
                log.warning(f'For {self.filename} there was no meta key: DateTime')
        return None

    @property
    def year(self):
        """
        :return: year of creation
        """
        if self.creation_datetime:
            return self.creation_datetime.year
        return -1

    @property
    def month(self):
        """
        :return: month of creation
        """
        if self.creation_datetime:
            return self.creation_datetime.month
        return -1

    @property
    def day(self):
        """
        :return: day of creation
        """
        if self.creation_datetime:
            return self.creation_datetime.day
        return -1

    @property
    def meta(self):
        """
        Meta data of the photo.
        """
        with self.__open_image() as image:
            exif = {ExifTags.TAGS[k]: v for k, v in image.getexif().items() if k in
                    ExifTags.TAGS}
            exif = {k: self._replace_empty(v) for k, v in exif.items()}

        return exif

    @property
    def path(self):
        """
        Returns path to photo file.
        """
        sub_path = f'{self.get_hash[:2]}/{self.get_hash}/{self.filename}'
        return f'{current_app.config[UPLOADED_PHOTOS_DEST_RELATIVE]}/{sub_path}'
