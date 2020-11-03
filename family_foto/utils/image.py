import os

from PIL import Image
from flask import current_app
from resizeimage.resizeimage import resize_width


def resize(path: str, filename: str, height: int, width: int):
    """
    Resizes an image to the ordered width,
    :param path: path to original image
    :param filename: name of the original image
    :param height: wanted height
    :param width: wanted width (aspect ration will be kept)
    :return: path to resized image
    """
    with open(path, 'rb') as file:
        with Image.open(file) as image:
            cover = resize_width(image, width)
            if not os.path.exists(current_app.config['RESIZED_DEST']):
                os.mkdir(current_app.config['RESIZED_DEST'])
            save_path = f'{current_app.config["RESIZED_DEST"]}/{width}_{height}_{filename}'
            cover.save(save_path, image.format)
    return save_path
