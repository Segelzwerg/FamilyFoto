from PIL import Image, ExifTags
from sqlalchemy import ForeignKey

from family_foto.config import BaseConfig
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
    def meta(self):
        """
        Meta data of the photo.
        """
        with Image.open(self.path) as image:
            exif = {ExifTags.TAGS[k]: v for k, v in image.getexif().items() if k in
                    ExifTags.TAGS}
            exif = {k: self._replace_empty(v) for k, v in exif.items()}

        return exif

    @property
    def path(self):
        """
        Returns path to photo file.
        """
        return f'{BaseConfig.UPLOADED_PHOTOS_DEST}/{self.filename}'

    def thumbnail(self, width: int, height: int):
        """
        Returns the url for resized photo.
        :param width: the new width
        :param height: the new height
        """
        save_path = resize(self.path, self.filename, height, width)
        return save_path.lstrip('.')
