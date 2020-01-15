# -*- coding: utf-8 -*-

from PIL import Image
import logging


def is_image(filename_in):
    try:
        Image.open(filename_in, mode='r')
        return True
    except:
        return False


# methods on images
def load_image(img_file):
    return Image.open(img_file, mode='r')


def to_rgb(im):
    if im.mode != 'RGB':
        return im.convert('RGB')
    else:
        return im


def save_as_jpeg(im, file_out, optimize=True, quality=95):
    im.save(file_out, "JPEG", optimize=optimize, quality=quality)


def get_ratio(size, max_size):
    if max_size == size or max_size == (0, 0):
        return 1.0
    else:
        return min(max_size[0] / size[0], max_size[1] / size[1])


def calculate_size(ratio: float, im):
    return int(ratio * im.width), int(ratio * im.height)


def resize_with_aspect(im, filename_in, max_size):
    ratio = get_ratio(im.size, max_size)
    new_size = calculate_size(ratio, im)
    logging.info(f"{filename_in} {im.size} will be changed to {new_size} @ ratio = {ratio}")
    resized = im.resize(new_size)
    return resized


def crop(im, xmin, ymin, xmax, ymax):
    return im.crop((xmin, ymin, xmax, ymax)).convert('RGB')
