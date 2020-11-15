import os

from PIL import Image, ExifTags
from flask import current_app
from sqlalchemy import ForeignKey

from family_foto.const import UPLOADED_PHOTOS_DEST_RELATIVE
from family_foto.models import db
from family_foto.models.file import File
from family_foto.utils.image import resize


class Photo(File):
    """
    Class of Photo Entity
    """

    id = db.Column(db.Integer, ForeignKey('file.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'photo'
    }

    @property
    def image_view(self):
        return f'/image/{self.filename}'

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
        return current_app.config[UPLOADED_PHOTOS_DEST_RELATIVE] + "/" + self.filename
