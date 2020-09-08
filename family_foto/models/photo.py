import os

from PIL import Image
from resizeimage.resizeimage import resize_width
from sqlalchemy import ForeignKey

from family_foto.config import BaseConfig
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

    def resize(self, width: int, height: int):
        """
        Returns the url for resized photo.
        :param width: the new width
        :param height: the new height
        """
        with open(self.path, 'r+b') as file:
            with Image.open(file) as image:
                cover = resize_width(image, width)
                if not os.path.exists(BaseConfig.RESIZED_DEST):
                    os.mkdir(BaseConfig.RESIZED_DEST)
                save_path = f'{BaseConfig.RESIZED_DEST}/{width}_{height}_{self.filename}'
                cover.save(save_path, image.format)
                image.close()
            file.close()
        return save_path.lstrip('.')
