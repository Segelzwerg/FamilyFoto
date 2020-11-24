import os

from cv2 import cv2
from flask import current_app

from family_foto.logger import log
from family_foto.models.file import File
from family_foto.models.photo import Photo
from family_foto.models.video import Video
from family_foto.utils import image


class ThumbnailService:
    """
    Creates thumbnails for a media file.
    """

    @staticmethod
    def generate(file: File, width=400, height=400):
        """
        Selects the resize function depending on the media type.
        :param file: to be resized
        :param width: the width of the thumbnail
        :param height: the height of the thumbnail
        :return: url to the thumbnail resource
        """
        log.info(f'Generate thumbnail for {file.filename}')
        if isinstance(file, Photo):
            path = image.resize(file.abs_path, file.filename, width, height)
        elif isinstance(file, Video):
            path = ThumbnailService.video_thumbnail(file, height, width)
        else:
            message = f'Thumbnail creation is not supported for {type(file)}.'
            log.error(message)
            raise TypeError(message)

        return f'/{os.path.relpath(path, os.path.dirname(current_app.config["RESIZED_DEST"]))}'

    @staticmethod
    def video_thumbnail(file, height, width):
        """
        Generates the thumbnail for a video.
        :param file: to be resized
        :param width: the width of the thumbnail
        :param height: the height of the thumbnail
        :return: url to the thumbnail resource
        """
        video = cv2.VideoCapture(file.abs_path)
        frame = image.get_random_frame(video)
        if frame is None:
            message = f'Could not read video: {file.abs_path}'
            log.error(message)
            raise IOError(message)
        path = f'{current_app.config["RESIZED_DEST"]}/{width}_{height}_{file.filename}.jpg'
        if not os.path.exists(current_app.config["RESIZED_DEST"]):
            os.mkdir(current_app.config["RESIZED_DEST"])
        if os.path.exists(path):
            log.warning(f'Thumbnail already exists: {path}')
            return path
        if not cv2.imwrite(path, frame):
            raise IOError(f'could not write {path}')
        path = image.resize(path, file.filename + '.jpg', width, height, force=True)
        video.release()
        cv2.destroyAllWindows()
        return path
