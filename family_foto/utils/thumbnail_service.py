import os
import random

from cv2 import cv2
from flask import current_app

from family_foto import log, RESIZED_DEST
from family_foto.models.file import File
from family_foto.models.photo import Photo
from family_foto.models.video import Video
from family_foto.utils.image import resize


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
            path = resize(file.abs_path, file.filename, width, height)
        elif isinstance(file, Video):
            path = ThumbnailService.video_thumbnail(file, height, width)
        else:
            message = f'Thumbnail creation is not supported for {type(file)}.'
            log.error(message)
            raise TypeError(message)

        return f'/{os.path.relpath(path, os.path.dirname(current_app.config["RESIZED_DEST"]))}'

    @staticmethod
    def video_thumbnail(file, height, width):
        video = cv2.VideoCapture(file.abs_path)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        video.set(cv2.CAP_PROP_POS_FRAMES, random.randint(0, frame_count))
        _, frame = video.read()
        if frame is None:
            message = f'Could no read video: {file.abs_path}'
            log.error(message)
            raise IOError(message)
        path = f'{current_app.config[RESIZED_DEST]}/{width}_{height}_{file.filename}.jpg'
        if not os.path.exists(current_app.config[RESIZED_DEST]):
            os.mkdir(current_app.config[RESIZED_DEST])
        if not cv2.imwrite(path, frame):
            raise IOError(f'could not write {path}')
        path = resize(path, file.filename, width, height)
        video.release()
        cv2.destroyAllWindows()
        return path
