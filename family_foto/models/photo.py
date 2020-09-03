from datetime import datetime

from PIL import Image, ExifTags
from sqlalchemy import ForeignKey

from family_foto.models import db


class Photo(db.Model):
    # pylint: disable=too-few-public-methods
    """
    Database entity of a photo.
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(128), unique=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.Integer, ForeignKey('user.id'))

    @property
    def path(self):
        """
        Path of the photo on the server.
        """
        return f'./photos/{self.filename}'

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

    @staticmethod
    def _replace_empty(value: bytes):
        """
        Tries to replace '\x00'
        """
        try:
            value = str(value).replace('\x00', '')
        finally:
            return str(value)
