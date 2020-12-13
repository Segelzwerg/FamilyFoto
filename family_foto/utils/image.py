import os

from PIL import Image
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
        save_path = os.path.join(os.path.dirname(path), f'{width}_{height}_{filename}')
        if not force and os.path.exists(save_path):
            log.warning(f'Thumbnail already exists: {save_path}')
            return save_path

        with Image.open(file) as image:
            cover = resize_width(image, width)
            cover.save(save_path, image.format)
    return save_path
