# -*- coding: utf-8 -*-
from handler.file import remove_file_safely, get_file_name, get_extension
from PIL import Image
import logging
from typing import Tuple

def is_image(filename_in: str)->bool:
    try:
        Image.open(filename_in, mode='r')
        return True
    except:
        return False

def image_size(path: str)-> Tuple[int, int]:
    try:
        with Image.open(path) as img:
            return img.size
    except:
        return None, None

def convert_to_jpeg_and_override(image_in):
    im = load_as_irg(image_in)
    remove_file_safely(image_in)
    new_name = get_file_name(image_in).replace(get_extension(image_in), ".jpg")
    save_as_jpeg(im, new_name)

# methods on images

def load_as_irg(img_file: str)-> Image.Image:
    im = load_image(img_file)
    im_rgb = to_rgb(im)
    return im_rgb

def load_image(img_file: str)-> Image.Image:
    return Image.open(img_file, mode='r')


def to_rgb(im: Image.Image)-> Image.Image:
    if im.mode == 'RGB':
        return im
    else:
        return im.convert('RGB')


def save_as_jpeg(im: Image.Image, file_out: str, optimize=True, quality=95)-> None:
    im.save(file_out, "JPEG", optimize=optimize, quality=quality)


def get_ratio(size: Tuple[int, int], max_size: Tuple[int, int])-> float:
    if max_size == size or max_size == (0, 0):
        return 1.0
    else:
        return min(max_size[0] / size[0], max_size[1] / size[1])


def calculate_size(ratio: float, im: Image.Image)-> Tuple[int, int]:
    return int(ratio * im.width), int(ratio * im.height)


def resize_with_aspect(im: Image.Image, filename_in: str, max_size: Tuple[int,int])-> Image.Image:
    ratio = get_ratio(im.size, max_size)
    new_size = calculate_size(ratio, im)
    logging.info(f"{filename_in} {im.size} will be changed to {new_size}\
                   @ ratio = {ratio}")
    resized = im.resize(new_size)
    return resized


def crop(im: int, xmin: int, ymin: int, xmax: int, ymax: int)-> Image.Image:
    return im.crop((xmin, ymin, xmax, ymax)).convert('RGB')
