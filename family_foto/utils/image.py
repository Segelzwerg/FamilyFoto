import os
import random

from PIL import Image
from cv2 import cv2
from flask import current_app
from resizeimage.resizeimage import resize_width

from family_foto.logger import log

def resize(path: str, filename: str, height: int, width: int, force: bool = False):
    """
    Resizes an image to the ordered width,
    :param path: path to original image
    :param filename: name of the original image
    :param height: wanted height
    :param width: wanted width (aspect ration will be kept)
    :param force: force recreation of thumbnail
    :return: path to resized image
    """
    with open(path, 'rb') as file:
        if not os.path.exists(current_app.config['RESIZED_DEST']):
            os.mkdir(current_app.config['RESIZED_DEST'])
        save_path = f'{current_app.config["RESIZED_DEST"]}/{width}_{height}_{filename}'
        if not force and os.path.exists(save_path):
            log.warning(f'Thumbnail already exists: {save_path}')
            return save_path

        with Image.open(file) as image:
            cover = resize_width(image, width)
            cover.save(save_path, image.format)
    return save_path


def get_random_frame(video):
    """
    Extracts a random frame from a video
    :param video: from which the frame should be extracted
    :return: one frame
    """
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video.set(cv2.CAP_PROP_POS_FRAMES, random.randint(0, frame_count))
    _, frame = video.read()
    return frame
