import os

from flask import current_app

from family_foto import log
from family_foto.models.file import File
from family_foto.models.photo import Photo
from family_foto.models.video import Video
from family_foto.utils.image import resize


class ThumbnailService:
    """
    Creates thumbnails for a media file.
    """
    @staticmethod
    def generate(file: File):
        """
        Selects the resize function depending on the media type.
        :param file: to be resized
        :return: url to the thumbnail resource
        """
        log.info(f'Generate thumbnail for {file.filename}')
        if isinstance(file, Photo):
            path = resize(file.abs_path, file.filename, 400, 400)
        elif isinstance(file, Video):
            pass
        else:
            message = f'Thumbnail creation is not supported for {type(file)}.'
            log.error(message)
            raise TypeError(message)

        return f'/{os.path.relpath(path, os.path.dirname(current_app.config["RESIZED_DEST"]))}'