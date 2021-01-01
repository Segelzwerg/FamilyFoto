import os
import random

import ffmpeg
from flask import current_app

from family_foto.logger import log
from family_foto.models.file import File
from family_foto.models.photo import Photo
from family_foto.models.video import Video
from family_foto.utils import image


async def generate_all(file_ids: [int], width: int, height: int):
    """
    Generates thumbnails for a it's files.
    """
    thumbnails = []
    files: [File] = File.query.filter_by(File.id.in_(file_ids)).all()
    for file in files:
        thumbnails.append(generate(file, width, height))
    return thumbnails


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
        path = video_thumbnail(file, height, width)
    else:
        message = f'Thumbnail creation is not supported for {type(file)}.'
        log.error(message)
        raise TypeError(message)

    uploaded_photos_dest = os.path.dirname(current_app.config["UPLOADED_PHOTOS_DEST"])
    return f'/{os.path.relpath(path, uploaded_photos_dest)}'


def video_thumbnail(file: Video, height: int, width: int):
    """
    Generates the thumbnail for a video.
    :param file: to be resized
    :param width: the width of the thumbnail
    :param height: the height of the thumbnail
    :return: url to the thumbnail resource
    """
    path = os.path.join(os.path.dirname(file.abs_path), f'{width}_{height}_{file.filename}.jpg')

    if os.path.exists(path):
        log.warning(f'Thumbnail already exists: {path}')
        return path

    frame = random.randint(0, file.frame_count)
    try:
        _resized_frame(file, frame, height, path, width)
    except ffmpeg.Error as error:
        raise IOError(f'Could not read frames from {path}') from error
    return path


def _resized_frame(file, frame, height, path, width):
    (ffmpeg.input(file.abs_path)
     .trim(start_frame=frame, end_frame=frame + 2)
     .output(path,
             s=f'{width}x{height}',
             frames='1')
     .run(capture_stdout=True,
          capture_stderr=False))
