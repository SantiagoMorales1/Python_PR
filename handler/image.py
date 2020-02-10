# -*- coding: utf-8 -*-
import logging
from typing import Tuple

from PIL import Image

from handler.file import remove_file_safely, get_extension


def is_image(filename_in: str) -> bool:
    """
This function tries to open the file provided using the Pillow framework.
    :param filename_in: file to be open as an image
    :return: True if the file can be treated as an  image or False if  pillow can't open the file.
    """
    try:
        Image.open(filename_in, mode='r')
        return True
    except:
        return False


def image_size(path: str) -> Tuple[int, int]:
    """
    Opens the image using the PIL framework and returns the size of the image.
    Args:
        path (str):

    Returns:

    """
    try:
        with Image.open(path) as img:
            return img.size
    except:
        return None, None


def convert_to_jpeg_and_override(image_in: str):
    im = load_as_rgb(image_in)
    new_name = image_in.replace(get_extension(image_in), ".jpg")
    remove_file_safely(image_in)
    save_as_jpeg(im, new_name)
    im.close()


# methods on images

def load_as_rgb(img_file: str) -> Image.Image:
    im = load_image(img_file)
    im_rgb = to_rgb(im)
    return im_rgb


def load_image(img_file: str) -> Image.Image:
    with Image.open(img_file, mode='r') as im:
        im.load()
        return im


def to_rgb(im: Image.Image) -> Image.Image:
    if im.mode == 'RGB':
        return im
    else:
        return im.convert('RGB')


def save_as_jpeg(im: Image.Image, file_out: str, optimize=True, quality=95) -> None:
    im.save(file_out, "JPEG", optimize=optimize, quality=quality)


def get_ratio(size: Tuple[int, int], max_size: Tuple[int, int]) -> float:
    if max_size == size or max_size == (0, 0):
        return 1.0
    else:
        return min(max_size[0] / size[0], max_size[1] / size[1])


def calculate_size(ratio: float, im: Image.Image) -> Tuple[int, int]:
    return int(ratio * im.width), int(ratio * im.height)


def resize_with_aspect(im: Image.Image, filename_in: str, max_size: Tuple[int, int]) -> Image.Image:
    ratio = get_ratio(im.size, max_size)
    new_size = calculate_size(ratio, im)
    logging.info(f"{filename_in} {im.size} will be changed to {new_size}\
                   @ ratio = {ratio}")
    resized = im.resize(new_size)
    return resized


def crop(im: int, xmin: int, ymin: int, xmax: int, ymax: int) -> Image.Image:
    """
Returns the section of a image between (xmin, y min ) y (xmax, ymax)
    :param im:
    :param xmin:
    :param ymin:
    :param xmax:
    :param ymax:
    :return:
    """
    return im.crop((xmin, ymin, xmax, ymax)).convert('RGB')
