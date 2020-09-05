import os
from datetime import datetime

from PIL import Image, ExifTags
from sqlalchemy import ForeignKey

from family_foto.models import db
from family_foto.models.user import User
from family_foto.resize import resize


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
    def abs_path(self):
        """
        Returns absolute path of the photo.
        """
        return os.path.abspath(f'/photo/{self.filename}')

    @property
    def image_view(self):
        """
        Returns path to image viewer template of this photo.
        """
        return f'/image/{self.filename}'

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
    def height(self):
        """
        Returns the image height.
        """
        return int(self.meta['ExifImageHeight'])

    @property
    def width(self):
        """
        Returns image width
        """
        return int(self.meta['ExifImageWidth'])

    def resize(self, width: int, height: int):
        """
        Returns the url for resized photo.
        :param width: the new width
        :param height: the new height
        """
        resized_url = resize(self.path, f'{width}x{height}')
        resized_url = resized_url.lstrip('.')
        return resized_url

    def has_read_permission(self, other_user: User) -> bool:
        """
        Checks if the other user has permission to view that photo.
        """
        if self.user == other_user.id:
            return True
        user = User.query.get(self.user)
        return user.has_general_read_permission(other_user)

    @staticmethod
    def _replace_empty(value: bytes):
        """
        Tries to replace '\x00'
        """
        return str(value).replace('\x00', '')
